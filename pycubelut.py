"""pycubelut v0.2
=== Author ===
Yoonsik Park
park.yoonsik@icloud.com
=== Description ===
A library and standalone tool to apply Adobe Cube LUTs to common image
formats. This supports applying multiple LUTs and batch image processing.
"""

import logging
import numpy as np
from colour.io.luts.iridas_cube import read_LUT_IridasCube, LUT3D, LUT3x1D
import os
from multiprocessing import Pool
from typing import Union


def read_lut(lut_path, clip=False):
    """
    Reads a LUT from the specified path, returning instance of LUT3D or LUT3x1D

    <lut_path>: the path to the file from which to read the LUT (
    <clip>: flag indicating whether to apply clipping of LUT values, limiting all values to the domain's lower and
        upper bounds
    """
    lut: Union[LUT3x1D, LUT3D] = read_LUT_IridasCube(lut_path)
    lut.name = os.path.splitext(os.path.basename(lut_path))[0]  # use base filename instead of internal LUT name

    if clip:
        if lut.domain[0].max() == lut.domain[0].min() and lut.domain[1].max() == lut.domain[1].min():
            lut.table = np.clip(lut.table, lut.domain[0, 0], lut.domain[1, 0])
        else:
            if len(lut.table.shape) == 2:  # 3x1D
                for dim in range(3):
                    lut.table[:, dim] = np.clip(lut.table[:, dim], lut.domain[0, dim], lut.domain[1, dim])
            else:  # 3D
                for dim in range(3):
                    lut.table[:, :, :, dim] = np.clip(lut.table[:, :, :, dim], lut.domain[0, dim], lut.domain[1, dim])

    return lut


def process_image(image_path, output_path, thumb, lut, log, no_prefix=False):
    """Opens the image at <image_path>, transforms it using the passed
    <lut> with trilinear interpolation, and saves the image at
    <output_path>, or if it is None, then the same folder as <image_path>.
    If <thumb> is greater than zero, then the image will be resized to have
    a max height or width of <thumb> before being transformed. Iff <log> is
    True, the image will be changed to log colorspace before the LUT.

    <image_path>: path to input image file
    <output_path>: path to output image folder
    <thumb>: max size for image dimension, 0 indicates no resizing
    <lut>: CubeLUT object containing LUT
    <log>: iff True, transform to log colorspace
    """
    from PIL import Image
    logging.info("Processing image: " + image_path)
    image_name, image_ext = os.path.splitext(image_path)
    if image_ext.lower() == '.tif' or image_ext.lower() == '.tiff':
        # im = tiff.imread(image_path)
        logging.warning("tiff file not supported yet, continuing...")
        return
    else:
        # attempt to open file as an image
        try:
            im = Image.open(image_path)
        except IOError:
            logging.info(image_path + " not an image file, continuing...")
            return
        if (im.mode != 'RGB'):
            im = im.convert('RGB')
        if thumb > 0:
            logging.debug("Resizing image: " + image_name)
            new_dims = (int(im.size[0] * thumb / max(im.size)),
                        int(im.size[1] * thumb / max(im.size)))
            im = im.resize(new_dims, Image.BICUBIC)
            image_ext = "_thumb" + image_ext
        logging.debug("Applying LUT: " + lut.name)
        im_array = np.asarray(im, dtype=np.float32) / 255
        is_non_default_domain = not np.array_equal(lut.domain, np.array([[0., 0., 0.], [1., 1., 1.]]))
        dom_scale = None
        if is_non_default_domain:
            dom_scale = lut.domain[1] - lut.domain[0]
            im_array = im_array * dom_scale + lut.domain[0]
        if log:
            im_array = im_array ** (1/2.2)
        im_array = lut.apply(im_array)
        if log:
            im_array = im_array ** (2.2)
        if is_non_default_domain:
            im_array = (im_array - lut.domain[0]) / dom_scale
        im_array = im_array * 255
        new_im = Image.fromarray(np.uint8(im_array))
        image_dir, image_filename = os.path.split(image_path)
        output_dir = output_path if output_path is not None else image_dir
        output_filename = lut.name + image_ext
        if not no_prefix:
            output_filename = os.path.basename(image_filename) + '_' + output_filename
        new_im.save(os.path.join(output_dir, output_filename), quality=95)

def main():
    # import tifffile as tiff
    import argparse
    import time
    import random

    parser = argparse.ArgumentParser(
        description="Tool for applying Adobe Cube LUTs to images\n\n"
                    "Output images are JPEGs (quality 95), named '<INPUT>_<LUT>.jpg' by default.")
    parser.add_argument("LUT",
                    help="Cube LUT filename/folder")
    parser.add_argument("INPUT",
                        help="input image filename/folder")
    parser.add_argument("-o", "--out",
                        help="output image folder")
    parser.add_argument("-np", "--no-prefix",
                        help="whether to not prefix output files with the image filename "
                             "(only possible if INPUT is not a directory)", action="store_true")
    parser.add_argument("-g", "--log",
                        help="convert to Log before LUT", action="store_true")
    parser.add_argument("-c", "--clip",
                        help="whether to clip LUT values to the domain's bounds, "
                             "which can fix issues with certain LUT exports", action="store_true")
    parser.add_argument("-v", "--verbose",
                        help="control verbosity and info messages",
                        action='append_const', const=1)
    parser.add_argument('-t', '--thumb', type=int, nargs='?', const=500,
                        default=0, help="resizes to <= 500px,"
                        " optionally specify max size")
    parser.add_argument("-j", "--jobs", type=int,
                         help="number of processes to spawn, defaults to "
                         "number of logical CPUs")
    args = parser.parse_args()
    args.verbose = 0 if args.verbose is None else sum(args.verbose)

    if args.verbose == 2:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose == 1:
        logging.basicConfig(level=logging.INFO,
                            format='%(levelname)s: %(message)s')
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s')

    luts = []
    start_time = time.time()

    # args.out is required if input is a folder
    if os.path.isdir(args.INPUT):
        if args.out is None:
            logging.error("For batch processing, output must be specified")
            exit(1)

    # Check if args.out is a valid folder
    if args.out is not None:
        args.out = os.path.join(args.out, '')
        if not os.path.isdir(args.out):
            logging.error(args.out + " not a folder or doesn't exist")
            exit(1)

    # determine if lut argument is a folder
    if os.path.isdir(args.LUT):
        # initialize all LUTs in folder
        args.LUT = os.path.join(args.LUT, '')
        for filename in os.listdir(args.LUT):
            file_path = os.path.join(args.LUT, filename)
            if not file_path.lower().endswith('.cube'):
                continue
            elif not os.path.isfile(file_path):
                continue
            else:
                luts.append(read_lut(file_path, clip=args.clip))
    else:
        # Exit if args.LUT is not a file
        if not os.path.isfile(args.LUT):
            logging.error(args.LUT + " doesn't exist")
            exit(1)
        # Single lut at <luts[0]>
        luts.append(read_lut(args.LUT, clip=args.clip))

    image_queue = []
    # determine if input is a folder
    if os.path.isdir(args.INPUT):
        args.INPUT = os.path.join(args.INPUT, '')
        # process all images in folder
        for filename in os.listdir(args.INPUT):
            file_path = os.path.join(args.INPUT, filename)
            if os.path.isfile(file_path):
                for lut in luts:
                    image_queue.append((file_path, args.out,
                        args.thumb, lut, args.log, args.no_prefix))
    else:
        # process single image
        for lut in luts:
            image_queue.append((args.INPUT, args.out,
                args.thumb, lut, args.log, args.no_prefix))

    logging.info("Starting pool with max " + str(len(image_queue))
                    + " tasks in queue")
    with Pool(processes=args.jobs, maxtasksperchild=20) as pool:
        random.shuffle(image_queue)
        pool.starmap(process_image, image_queue)

    end_time = time.time()

    logging.info("Completed in" + '% 6.2f' % (end_time - start_time) + "s")


__all__ = ['process_image', 'read_lut']


# Command Line Interface
if __name__ == "__main__":
    main()
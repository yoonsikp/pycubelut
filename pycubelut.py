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
from colour.io.luts.iridas_cube import read_LUT_IridasCube
import os
from multiprocessing import Pool


def process_image(image_path, output_path, thumb, lut, log):
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
        if log:
            im_array = im_array ** (1/2.2)
        im_array = lut.apply(im_array)
        if log:
            im_array = im_array ** (2.2)
        im_array = im_array * 255
        new_im = Image.fromarray(np.uint8(im_array))
        if output_path is None:
            new_im.save(image_name + '_' + lut.name + image_ext,
                        quality=95)
        else:
            new_im.save(output_path + os.path.basename(image_name) +
                        '_' + lut.name + image_ext, quality=95)

def main():
    # import tifffile as tiff
    import argparse
    import time
    import random

    parser = argparse.ArgumentParser(
        description="Tool for applying Adobe Cube LUTs to images")
    parser.add_argument("LUT",
                    help="Cube LUT filename/folder")
    parser.add_argument("INPUT",
                        help="input image filename/folder")
    parser.add_argument("-o", "--out",
                        help="output image folder")
    parser.add_argument("-g", "--log",
                        help="convert to Log before LUT", action="store_true")
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
                luts.append(read_LUT_IridasCube(file_path))
    else:
        # Exit if args.LUT is not a file
        if not os.path.isfile(args.LUT):
            logging.error(args.LUT + " doesn't exist")
            exit(1)
        # Single lut at <luts[0]>
        luts.append(read_LUT_IridasCube(args.LUT))

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
                        args.thumb, lut, args.log))
    else:
        # process single image
        for lut in luts:
            image_queue.append((args.INPUT, args.out,
                args.thumb, lut, args.log))

    logging.info("Starting pool with max " + str(len(image_queue))
                    + " tasks in queue")
    with Pool(processes=args.jobs, maxtasksperchild=20) as pool:
        random.shuffle(image_queue)
        pool.starmap(process_image, image_queue)

    end_time = time.time()

    logging.info("Completed in" + '% 6.2f' % (end_time - start_time) + "s")


__all__ = ['process_image']


# Command Line Interface
if __name__ == "__main__":
    main()
"""pycubelut v0.1
=== Author ===
Yoonsik Park
park.yoonsik@icloud.com
=== Description ===
A library and standalone tool to apply Adobe Cube LUTs to common image
formats. This supports applying multiple LUTs and batch image processing.
The CubeLUT class has complete Cube LUT parsing and transform capabilities.
"""

import logging
import numpy as np
from colour.algebra.interpolation import table_interpolation_tetrahedral, \
    table_interpolation_trilinear
from scipy.interpolate import RegularGridInterpolator
import os


class CubeLUT:
    """This class holds Cube LUT data and methods to apply the LUT to 2D RGB
    numpy arrays. This class only supports 3D LUTs.
    === Attributes ===
    filename:
        Filename of the Cube LUT
    title:
        A self-description of the Cube LUT extracted from the file
    data:
        numpy array containing the actual LUT, with dimensions:
        (self.size, self.size, self.size, 3). Initial RGB values can be
        transformed as follows: [Red, Green, Blue, :] -> Ordered RGB values
    size:
        The LUT is a cube with dimensions of equal size: <self.size>.
    dim:
        The number of dimensions of the LUT. This class only supports 3D LUTs.
    domain_min:
        A tuple containing the lowest RGB values supported by the LUT, 
        respectively.
    domain_max
        A tuple containing the highest RGB values supported by the LUT, 
        respectively.
    """

    def __init__(self, lut_path):
        """Initialize a CubeLUT class.

        <lut_path> must be a valid path to a .cube file
        """
        self.data = None
        self.dim = 0
        self.size = 0
        self.title = ""
        self.filename = ""
        self.domain_min = (0., 0., 0.)
        self.domain_max = (1., 1., 1.)
        self._read_cube_lut(lut_path)

    def _read_cube_lut(self, lut_path):
        """Internal function to parse Cube LUT files and initialize class
        variables.

        <lut_path> must be a valid path to a .cube file
        """
        logging.debug("Importing lut: " + lut_path)
        self.filename = lut_path
        lut_data = []
        with open(lut_path, 'r') as lut_file:
            for line in lut_file.readlines():
                if line[0] == '#' or line.strip() == '':
                    # skip comment/empty line
                    continue
                if "TITLE" in line:
                    self.title = ' '.join(line.split()[1:])
                elif "DOMAIN_MIN" in line:
                    self.domain_min = tuple(float(x) for x in line.split()[1:])
                elif "DOMAIN_MAX" in line:
                    self.domain_max = tuple(float(x) for x in line.split()[1:])
                elif "LUT_1D_SIZE" in line:
                    self.dim = 1
                    self.size = int(line.split()[1])
                    raise Exception('1D not supported: ' + self.filename)
                    # assert self.size <= 65536 and self.size >= 2
                elif "LUT_3D_SIZE" in line:
                    self.dim = 3
                    self.size = int(line.split()[1])
                    # assert self.size <= 256 and self.size >= 2
                else:
                    lut_data.append([float(num) for num in line.split()])
        # convert self.data to numpy format
        self.data = np.array(lut_data)
        x = self.size
        self.data = self.data.reshape([x, x, x, 3], order='F')
        if self.domain_min != (0., 0., 0.) or self.domain_max != (1., 1., 1.):
            logging.warn("nonstandard domain for LUT, output may be wrong")

    def transform_tetrahedral(self, image, in_place=False):
        """Returns the transformed <image>, using the LUT from <self.data>.
        This uses tetrahedral interpolation, which is more accurate and
        slower than trilinear interpolation. If <in_place> is True, the 
        <image> array will be directly modified.

        <image> is the 2D RGB array (i.e. 3D array)
        <in_place> specifies if <image> should be transformed directly
        """
        if not in_place:
            image = np.copy(image)

        for i, row in enumerate(image):
            image[i] = table_interpolation_tetrahedral(row, self.data)
        return image

    def transform_trilinear(self, image, in_place=False):
        """Returns the transformed <image>, using the LUT from <self.data>.
        This uses trilinear interpolation, which is faster than tetrahedral
        interpolation. If <in_place> is True, the <image> array will be
        directly modified.

        <image> is the 2D RGB array (i.e. 3D array)
        <in_place> specifies if <image> should be transformed directly
        """
        if not in_place:
            image = np.copy(image)

        for i, row in enumerate(image):
            image[i] = table_interpolation_trilinear(row, self.data)
        return image

    def _buggy_transform_trilinear(self, image, in_place=False):
        """Trilinear interpolation using scipy interpolation methods. Slower
        than the <transform_trilinear> method, and has bugs.

        <image> is the 2D RGB array (i.e. 3D array)
        <in_place> specifies if <image> should be transformed directly
        """
        if not in_place:
            image = np.copy(image)

        # save image shape for later
        orig_image_shape = image.shape
        # change 2D RGB -> 1D RGB
        image = image.reshape([-1, 3])
        # equally spaced grid from 0 to 1
        x = np.linspace(0, 1, self.size)
        # for RGB channels respectively
        for i in [0, 1, 2]:
            i_func = RegularGridInterpolator((x, x, x), self.data[:, :, :, i])
            image[:, i] = i_func(image[:])
        return image.reshape(orig_image_shape)


# Command Line Interface
if __name__ == "__main__":
    from PIL import Image
    # import tifffile as tiff
    import argparse
    import time

    parser = argparse.ArgumentParser(
        description="Tool for applying Adobe Cube LUTs to images")
    parser.add_argument("input",
                        help="input image filename/folder")
    parser.add_argument("-l", "--lut",
                        help="Cube LUT filename/folder", required=True)
    parser.add_argument("-o", "--outfolder",
                        help="output image folder")
    parser.add_argument("-g", "--log",
                        help="convert to Log before LUT", action="store_true")
    parser.add_argument("-v", "--verbose",
                        help="control verbosity and info messages",
                        action='append_const', const=1)
    parser.add_argument('-t', '--thumb', type=int, nargs='?', const=500,
                        default=0, help="resizes to <= 500px,"
                        " optionally specify max size")
    # parser.add_argument("-j", "--jobs", type=int, default=1,
    #                     help="number of processes to spawn, defaults to 1")
    args = parser.parse_args()
    args.verbose = 0 if args.verbose is None else sum(args.verbose)

    if args.verbose == 2:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose == 1:
        logging.basicConfig(level=logging.INFO,
                            format='%(levelname)s: %(message)s')
    else:
        logging.basicConfig(format='%(levelname)s: %(message)s')

    def process_image(image_path):
        """Opens the image at <image_path>, transforms it using all available
        luts in the global <luts> variable with trilinear interpolation,
        and saves the image in <args.outfolder> or the same folder as the
        image if <args.outfolder> doesn't exist. If <args.thumb> is specified,
        then the image will be resized before being transformed.

        <image_path>: path to the image file
        """
        logging.info("Processing image: " + image_path)
        image_name, image_ext = os.path.splitext(image_path)
        if image_ext.lower() == '.tif' or image_ext.lower() == '.tiff':
            # im = tiff.imread(image_path)
            logging.warn("tiff file not supported yet, continuing...")
            return
        else:
            # attempt to open file as an image
            try:
                im = Image.open(image_path)
            except IOError:
                logging.warn(image_path + " not an image file, continuing...")
                return
            if (im.mode != 'RGB'):
                im = im.convert('RGB')
            if args.thumb > 0:
                logging.debug("Resizing image: " + image_name)
                new_dims = (int(im.size[0] * args.thumb / max(im.size)),
                            int(im.size[1] * args.thumb / max(im.size)))
                im = im.resize(new_dims, Image.BICUBIC)
                image_ext = "_thumb" + image_ext
            for lut in luts:
                logging.debug("Applying LUT: " + lut.filename)
                im_array = np.asarray(im, dtype=np.float32) / 255
                if args.log:
                    im_array = im_array ** (1/2.2)
                lut.transform_trilinear(im_array, in_place=True)
                if args.log:
                    im_array = im_array ** (2.2)
                im_array = im_array * 255
                new_im = Image.fromarray(np.uint8(im_array))
                lutname = os.path.split(lut.filename)[1][:-5].replace(' ', '_')
                if args.outfolder is None:
                    new_im.save(image_name + '_' + lutname + image_ext,
                                quality=95)
                else:
                    new_im.save(args.outfolder + os.path.basename(image_name) +
                                '_' + lutname + image_ext, quality=95)

    luts = []
    start_time = time.time()

    # outfolder is required if input is a folder
    if os.path.isdir(args.input):
        if args.outfolder is None:
            logging.error("For batch processing, output must be specified")
            exit(1)

    # Check if outfolder is a valid folder
    if args.outfolder is not None:
        args.outfolder = os.path.join(args.outfolder, '')
        if not os.path.isdir(args.outfolder):
            logging.error(args.outfolder + " not a folder or doesn't exist")
            exit(1)

    # determine if lut argument is a folder
    if os.path.isdir(args.lut):
        # initialize all LUTs in folder
        args.lut = os.path.join(args.lut, '')
        for filename in os.listdir(args.lut):
            file_path = os.path.join(args.lut, filename)
            if not file_path.lower().endswith('.cube'):
                continue
            elif not os.path.isfile(file_path):
                continue
            else:
                luts.append(CubeLUT(file_path))
    else:
        # Exit if args.lut is not a file
        if not os.path.isfile(args.lut):
            logging.error(args.lut + " doesn't exist")
            exit(1)
        # Single lut at <luts[0]>
        luts.append(CubeLUT(args.lut))

    # determine if input is a folder
    if os.path.isdir(args.input):
        args.input = os.path.join(args.input, '')
        # process all images in folder
        for filename in os.listdir(args.input):
            file_path = os.path.join(args.input, filename)
            if os.path.isfile(file_path):
                process_image(file_path)
    else:
        # process single image
        process_image(args.input)

    end_time = time.time()

    logging.info("Completed in" + '% 6.2f' % (end_time - start_time) + "s")

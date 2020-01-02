# pycubelut
[![GitHub license](https://img.shields.io/github/license/yoonsikp/pycubelut.svg)](https://github.com/yoonsikp/pycubelut/blob/master/LICENSE)

Stop wasting time with sloppy 'gram filters, and use `pycubelut` to easily add that *pro* feel to your images!

## Quick Start
Download one of many free `.cube` LUTs online \[[1](https://luts.iwltbap.com/#freeware), [2](https://www.freepresets.com/product/free-luts-cali-vibes/)\]. Then, run the following with your downloaded LUT and image.

```
$ pip3 install pycubelut
$ cubelut F-8700-V2-STD.cube P1040326.jpg -v
INFO: Processing image: P1040326.jpg
INFO: Completed in  6.71s
```

## Sample Image
<p align="center">
  <img src=https://github.com/yoonsikp/pycubelut/blob/master/sample.jpg?raw=true width=100%>
</p>

## Overview
Many professionals apply 3D LUTs to obtain a certain look and feel to their images and videos, which is usually done with proprietary software such as Adobe Photoshop or Final Cut Pro. `pycubelut` was created to be the first easy to use, open-source, command-line tool to apply Adobe Cube LUTs to images.

In the context of images, a Lookup Table (LUT) is a table describing a transformation of RGB values. There are multiple types of LUTs used in image processing, most common being 1D LUTs and 3D LUTs. A 1D LUT contains an independent transformation for each colour channel, meaning there would be three 1D LUTs defined (for Red, Green, and Blue). However, a 3D LUT has every colour in RGB space directly mapped to another specified colour (ℝ³ -> ℝ³), allowing for powerful and arbitrary transformations, such as greyscale, false colour, and hue shifts. All colour effects, such as gamma, contrast, brightness, etc. can be encoded as a 3D LUT.

3D LUTs are essentially grids in the shape of cubes (hence Adobe used `.cube` for their LUT file extension). In order to encode a lossless transformation of the complete 8 bit RGB space, 256x256x256 mappings are needed. However, the Cube format allows for interpolation of values from a LUT defined with fewer points, commonly 33x33x33 mappings.

## Usage
Warning: If your input image is in a Log colorspace, make sure to choose a Log LUT!
```
$ cubelut --help
usage: cubelut [-h] [-o OUT] [-g] [-v] [-t [THUMB]] [-j JOBS] LUT INPUT

Tool for applying Adobe Cube LUTs to images

positional arguments:
  LUT                   Cube LUT filename/folder
  INPUT                 input image filename/folder

optional arguments:
  -h, --help            show this help message and exit
  -o OUT, --out OUT     output image folder
  -g, --log             convert to Log before LUT
  -v, --verbose         control verbosity and info messages
  -t [THUMB], --thumb [THUMB]
                        resizes to <= 500px, optionally specify max size
  -j JOBS, --jobs JOBS  number of processes to spawn, defaults to number of
                        logical CPUs
```

### Multiple LUTs
Applies all `.cube` files in the folder to the image(s)
```
$ cubelut ./my_luts/ P1040326.jpg -v
```

### Batch Image Processing
Processes all images in the input folder, and outputs to a specified folder
```
$ cubelut ./my_luts/ ./my_images/ -o ./new_images/ -v
```

### Thumbnail Mode
Resizes images for a huge speedup, useful for multiple LUTs
```
$ cubelut ./my_luts/ P1040326.jpg -v -t
```

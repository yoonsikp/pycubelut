# pycubelut
Stop wasting time with sloppy 'gram filters, and use `pycubelut` to easily add that "pro" feel to your images!

## Quick Start
```
$ python3 pycubelut.py --lut F-8700-V2-STD.cube P1040326.jpg -v
INFO: Processing image: P1040326.jpg
INFO: Completed in  6.71s
```

## Sample Image
<p align="center">
  <img src=https://github.com/yoonsikp/pycubelut/blob/master/sample.jpg?raw=true width=100%>
</p>

## Detailed Explanation
In the context of images/video, a Look Up Table, or LUT, is an encoding of a transformation from one RGB value to another. There are two types of LUTs used in image processing, 1D LUT and 3D LUT. A 1D LUT contains an individual transformation for each colour channel, so for an image there would be three 1D LUTs (for Red, Green, and Blue). However, a 3D LUT is much more powerful, allowing for arbitrary transformations, such as hue shifts, greyscale, false colour, and other complex effects. This is because a 3D LUT has every point of RGB space directly mapped to another specified colour (ℝ³ -> ℝ³). All possible colour effect such as gamma, saturation, contrast, brightness, etc. can be encoded into a 3D LUT.

3D LUTs are essentially grids in the shape of cubes, the reason why Adobe used `.cube` for their LUT file extension. In order to encode the transformation of a complete 8 bit RGB space, 256x256x256 = 17 million mappings are required. However, the Cube format allows for interpolation of expected values from a LUT defined with an arbitrary level of precision, such as a LUT with only 33x33x33 = 36 thousand mappings.

Many professionals use 3D LUTs to obtain a certain look to their images and videos, although this is usually done using proprietary software such as Adobe Photoshop or Final Cut Pro. `pycubelut` was thus created to be the first free, easy to use, open-source, command-line tool to apply Adobe Cube LUTs to images.

## Usage
```
$ python3 pycubelut.py --help
usage: pycubelut.py [-h] -l LUT [-o OUTFOLDER] [-g] [-v] [-t [THUMB]] input

Tool for applying Adobe Cube LUTs to images

positional arguments:
  input                 input image filename/folder

optional arguments:
  -h, --help            show this help message and exit
  -l LUT, --lut LUT     Cube LUT filename/folder
  -o OUTFOLDER, --outfolder OUTFOLDER
                        output image folder
  -g, --log             convert to Log before LUT
  -v, --verbose         control verbosity and info messages
  -t [THUMB], --thumb [THUMB]
                        resizes to <= 500px, optionally specify max size
```


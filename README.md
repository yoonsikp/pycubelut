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
In the context of images and video, a Lookup Table (LUT) is a table describing a mapping/transformation of RGB values. There are multiple types of LUTs used in image processing, although most common are 1D LUTs and 3D LUTs. A 1D LUT contains an independent transformation for each colour channel, so in this case there would be three 1D LUTs (for Red, Green, and Blue). However, a 3D LUT is more powerful and allows for arbitrary transformations, such as greyscale, false colour, and other complex effects. This is because a 3D LUT has every colour in RGB space directly mapped to another specified colour (ℝ³ -> ℝ³). All colour effects such as gamma, saturation, contrast, brightness, etc. can be encoded as a 3D LUT.

3D LUTs are essentially grids in the shape of cubes (why Adobe used `.cube` for their LUT file extension). In order to encode the transformation of a complete 8 bit RGB space, 256x256x256 = 17 million mappings are required. However, the Cube format allows for interpolation of values from a LUT defined with a fewer number of points, such as a LUT with only 33x33x33 = 36 thousand mappings.

Many professionals apply 3D LUTs to obtain a certain look to their images and videos, and this is usually done with proprietary software such as Adobe Photoshop or Final Cut Pro. `pycubelut` was created to be the first free, easy to use, open-source, command-line tool to apply Adobe Cube LUTs to images.

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

### Multiple LUTs
Applies all `.cube` files in the folder to the image(s)
```
$ python3 pycubelut.py --lut ./my_luts/ P1040326.jpg -v
```

### Batch Image Processing
Processes all images in the input folder, and outputs to a specified folder
```
$ python3 pycubelut.py --lut ./my_luts/ -o ./new_images/ ./my_images/ -v
```

### Thumbnail Mode
Resizes images for a huge speedup, useful for Multiple LUTs
```
$ python3 pycubelut.py --lut ./my_luts/ P1040326.jpg -v -t
```

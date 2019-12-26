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


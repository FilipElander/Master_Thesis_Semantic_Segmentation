
# Script for image mirroring an entire folder 
## USAGE ##
# Temrinal arguments: Input_folder  output_folder file_type
# Example: augment.py /Desktop/input Desktop/output png


# Dependencies
from glob import glob
from PIL import Image, ImageOps
from pathlib import Path 
import sys

## input and output directory 
in_dir = sys.argv[1]
out_dir = sys.argv[2]
fileType = sys.argv[3] # file type

IMAGE_FILES = sorted(glob(in_dir + '/*.'+fileType))
c = 0
for image_file in IMAGE_FILES:
    image_name =Path(image_file).name 
    im = Image.open(image_file)
    im_mirror = ImageOps.mirror(im)
    im_mirror.save(out_dir+"/"+image_name)
    c = c+1



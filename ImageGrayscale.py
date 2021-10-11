# Script for converting images in a folder into Grayscale
## USAGE ##
# Temrinal arguments: Input_folder  output_folder file_type
# Example: augment.py /Desktop/input Desktop/output png

# Dependencies
from glob import glob
from PIL import Image
from pathlib import Path 
import sys

in_dir = sys.argv[1]
out_dir = sys.argv[2]
fileType = sys.argv[3] 

IMAGE_FILES = sorted(glob(in_dir + '/*.'+fileType))
for image_file in IMAGE_FILES:
    image_name =Path(image_file).name 
    im = Image.open(image_file)
    im.convert('L').save(out_dir+"/"+image_name) 


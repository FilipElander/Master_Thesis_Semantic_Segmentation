## Script for changing between png and jpg

## USAGE ##
# Temrinal arguments: Input_folder  output_folder from_format to_format 
# Example: ImageFormatChanger.py /Desktop/input Desktop/output png jpg


from glob import glob
from PIL import Image 
import os
from pathlib import Path 
import sys

## Input Arguments  
in_dir = sys.argv[1] # Input folder 
out_dir = sys.argv[2] # Output folder
from_format = sys.argv[3] 
to_format = sys.argv[4] 


IMAGE_FILES = sorted(glob(in_dir + '/*.' + from_format))
c = 1

for image_file in IMAGE_FILES:
    print("image",c)
    image_name =Path(image_file).name
    name =os.path.splitext(image_name)[0] 
    im = Image.open(image_file)
    rgb_im = im.convert('RGB')
    rgb_im.save(out_dir+"/"+name+'.' + to_format)
    
    c = c+1
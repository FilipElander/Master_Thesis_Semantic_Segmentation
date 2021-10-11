# Script for overlaying two images 

## Input arguments 
## USAGE ##
# Temrinal arguments: First_image Second_image alpha/transparency result_file_name file_type
# Example: ImageBlending.py /Desktop/0001.png Desktop/0002.png 0.5 blended png
 
# Dependencies
import sys
from PIL import Image 

## input and output directory 
first_im = sys.argv[1]
second_im = sys.argv[2]
alpha_val = float(sys.argv[3]) 
name= sys.argv[4]
file_type = sys.argv[5]

im1 = Image.open(first_im)
im2 = Image.open(second_im)
im = Image.blend(im1,im2,alpha=alpha_val)
im.save(name+'.'+file_type)
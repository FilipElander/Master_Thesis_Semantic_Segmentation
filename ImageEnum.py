
# Script for image enumerating an entire folder 
## USAGE ##
# Temrinal arguments: Input_folder  output_folder file_type
# Example: augment.py /Desktop/input Desktop/output png


from glob import glob
from PIL import Image
from pathlib import Path 
import sys

## Input Arguments  
in_dir = sys.argv[1] # Input folder 
out_dir = sys.argv[2] # Output folder 
fileType = sys.argv[3] # file type

#change between png and jpg
IMAGE_FILES = sorted(glob(in_dir + '/*.' + fileType))
c = 0
for image_file in IMAGE_FILES:
    image_name =Path(image_file).name 
    im = Image.open(image_file)	
    name = str(c).zfill(4) # fill with zeros 4 charachters long
    im.save(out_dir+"/"+name + "." + fileType)
    c = c+1


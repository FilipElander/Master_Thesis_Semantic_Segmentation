## Script for cropping images in an entire folder
# used for fitting a dataset for Machine Learning Network  
# The script crops from centre of the image 
## USAGE ##
# Temrinal arguments: Input_folder  output_folder widht height file_type
# Example: ImageCrop.py /Desktop/input Desktop/output 320 320 png


from glob import glob
from PIL import Image 
from pathlib import Path 
import sys

## Input Arguments  
in_dir = sys.argv[1] # Input folder 
out_dir = sys.argv[2] # Output folder 
fileType = sys.argv[5] # file type

WIDHT = int(sys.argv[3])
HEIGHT = int(sys.argv[4])
print("WIDTH",WIDHT)
print("HEIGHT",HEIGHT)
#change between png and jpg
IMAGE_FILES = sorted(glob(in_dir + '/*.'+ fileType))
c = 0
print("image")
for image_file in IMAGE_FILES:
    print(c)
    image_name =Path(image_file).name 
    name, form = image_name.rsplit('.', 1)
   
    im = Image.open(image_file)
    original_widht , original_height = im.size
    print("original width",original_widht)
    print("original height",original_height)
    # making sure the image isn't smaller than what we are trying to crop it into (Error checking)
    if original_widht >= WIDHT and original_height >= HEIGHT:
        # Cropped image of above dimension
        x = int(round((original_widht/2) - (WIDHT/2)))
        print("x",x)
        y = int(round((original_height/2) - (HEIGHT/2)))
        print("y",y)
        im1 = im.crop((x, y, x+ WIDHT, y+  HEIGHT))
        im1.save(out_dir+"/"+name + "."+fileType)
  
    c = c+1





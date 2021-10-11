
## Script for Changing segmented single channel grayscale images containing 5 classes 
# to 3 channeld RGB images
# Must be in PNG format    
# used for displaying the inferenced results 
## USAGE ##
# Temrinal arguments: Input_folder  output_folder 
# Example: ImageGrayscale2RGB.py /Desktop/input Desktop/output 

# Dependencies
import numpy as np
from PIL import Image 
from glob import glob
from PIL import Image, ImageEnhance 
import os
import numpy as np
from pathlib import Path
import sys

## Input Arguments  
in_dir = sys.argv[1] # Input folder 
out_dir = sys.argv[2] # Output folder 


# COLORS 
RED = (255,0,0)
DARK_GREEN = (0,100,0)
BLUE = (50,50,250)
LIGHT_GREEN = (0,200,0)
YELLOW = (200,200,0)
# CLASSES  

OBSTACLE = RED
FOILAGE = DARK_GREEN
SKY = BLUE 
GRASS = LIGHT_GREEN
TRAIL = YELLOW

color = [OBSTACLE,FOILAGE,SKY,GRASS,TRAIL]
#color = [(255,0,0),(0,100,0),(50,50,250),(0,200,0),(200,200,0)]

classes = 5
format = "png"
IMAGE_FILES = sorted(glob(in_dir + '/*.'+format))
c = 1

for image_file in IMAGE_FILES:
    print("image",c)
    c +=1
    image_name =Path(image_file).name
    name =os.path.splitext(image_name)[0] 
    im = Image.open(image_file)
    values, counts = np.unique(im, return_counts=True)
    print(im.format, im.size,im.mode)
    H = im.size[0]
    W = im.size[1]
    print(values)
    print(counts)
    newim = np.array(im)
    segmented_img = np.zeros((W,H,3)) 

    for x in range(W):
        for y in range(H):
            pixel = newim[x,y]
            if pixel == 0:
                segmented_img[x,y,0] = color[0][0]
                segmented_img[x,y,1] = color[0][1]
                segmented_img[x,y,2] = color[0][2]
            if pixel == 96:
                segmented_img[x,y,0] = color[1][0]
                segmented_img[x,y,1] = color[1][1]
                segmented_img[x,y,2] = color[1][2]
            if pixel == 100:
                segmented_img[x,y,0] = color[2][0]
                segmented_img[x,y,1] = color[2][1]
                segmented_img[x,y,2] = color[2][2]
            if pixel == 150:
                segmented_img[x,y,0] = color[3][0]
                segmented_img[x,y,1] = color[3][1]
                segmented_img[x,y,2] = color[3][2]
            if pixel == 170:
                segmented_img[x,y,0] = color[4][0]
                segmented_img[x,y,1] = color[4][1]
                segmented_img[x,y,2] = color[4][2]      
            else:
                pass
    im = Image.fromarray(np.uint8(segmented_img)).convert('RGB')
    im.save(out_dir+"/"+name.zfill(4)+'.png',"PNG") 


# Script that converts the 3 channel RGB and blurred lines inferenced results from the 
# Nvidia Jetson into single channel grayscale images containing only the avalible pixel classes   

## This is a preprocessing script that enables the dataset to be compared against the ground truth
#  images that the network has been trained on. 

## USAGE ##
# Temrinal arguments: Input_folder  output_folder 
# Example: NetworkJetsonRGB2GSMask.py /Desktop/input Desktop/output 



from glob import glob
from PIL import Image, ImageEnhance 
import os
import numpy as np
from pathlib import Path
import sys

## Global variable 
THRESHOLD = 65 # the threshold value for the pixel to either be pushed to 0 or 128 in the RGB scale

## Input Arguments  
in_dir = sys.argv[1] # Input folder 
out_dir = sys.argv[2] # Output folder


IMAGE_FILES = sorted(glob(in_dir + '/*.jpg'))
c = 1
for image_file in IMAGE_FILES:
    print("image",c)
    c +=1
    image_name =Path(image_file).name
    name =os.path.splitext(image_name)[0] 
    im = Image.open(image_file)

    newim = np.array(im)
    w, h = im.size

###############################  FILTERS ##############################################
    # checks every pixel in the image and pushes its RGB channel to either max or min
    # filtering out the blured lines and forces the pixels to the same values 
    for x in range(w):
        for y in range(h):
                dist = newim[x,y]
                R = dist[0]
                G = dist[1]
                B = dist[2]
                if R<THRESHOLD:
                        R = 0 
                if G<THRESHOLD:
                        G = 0
                if B<THRESHOLD:
                        B = 0 

                if R>=THRESHOLD:
                        R = 128
                if G>=THRESHOLD:
                        G = 128
                if B>=THRESHOLD:
                        B = 128

                newim[x,y]=[R,G,B]  

    # For the extreme cases of black and white, the filter will push the black to red and the white to magenhtha 
    for x in range(w):
        for y in range(h):
                dist = newim[x,y]
                if np.sum(dist) == 0:
                        newim[x,y]=[128,0,0]
                if np.sum(dist) == 128*3:
                        newim[x,y]=[0,128,128]


###############################  GRAYSCALE CONVERTER  ##############################################
# The image is converted into grayscale and the resulting pixel values are changed to the corresponding 
# values used in the trainng set and ground truth. so the result can be evaluated to the ground truth  
    RGB = Image.fromarray(newim.astype('uint8'), 'RGB')
    RGB.save('RGB.png',"PNG") 
    grey_im = RGB.convert('L')
    newim = np.array(grey_im)
    X, Y = newim.shape     
    for x in range(X):
        for y in range(Y):
            pixel = newim[x,y]
            if pixel == 15: # object class 
                newim[x,y] = 150
            if pixel == 38: # object class 
                newim[x,y] = 96
            if pixel == 53: # object class 
                newim[x,y] = 170
            if pixel == 90: # object class 
                newim[x,y] = 0 
            if pixel == 113: # object class 
                newim[x,y] = 100

    converted_im = Image.fromarray(newim) 
    converted_im.save(out_dir+"/"+name.zfill(4)+'.png',"PNG")                                       
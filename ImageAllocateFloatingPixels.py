# Script for forcing floating pixels into a certain pixelvalue/Threshold value.
# used for making sure no floating pixels occures in the images.
# floating pixels could give false statistics and faulty training in machine learning when the 
# pixelvalues indicates a class. 

from glob import glob
import os
import os.path
from PIL import Image
import numpy as np
from pathlib import Path
import sys

# Pixel/class Thresholds
th1 = 0
th2 = 96
th3 = 100
th4 = 150
th5 = 170

## Input Arguments  
in_dir = sys.argv[1] # Input folder 
out_dir = sys.argv[2] # Output folder 
fileType = sys.argv[3] # file type

amount = 0
IMAGE_FILES = sorted(glob(in_dir + '/*.'+fileType))
print("image")
c =1
for image_file in IMAGE_FILES:
    print(c)
    image_name =Path(image_file).name 
    im = Image.open(image_file)
    newim = np.array(im)
    X, Y = newim.shape
    for x in range(X):
        for y in range(Y):
            pixel = newim[x,y]
            if pixel < th2:
                newim[x,y] = th1
            if th2 <= pixel < th3:
                newim[x,y] = th2
            if th3 <= pixel < th4:
                newim[x,y] = th3
            if th4 <= pixel < th5:
                newim[x,y] = th4
            if th5 <= pixel:
                newim[x,y] = th5
            
            else:
                pass
    
    conim = Image.fromarray(newim)
    conim.save(out_dir+"/"+image_name)
    
    c = c+1
print("FINISHED")        
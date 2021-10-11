
# This script will take a Ground Truth dataset and compare it to inferenced results from a semantic segmentation network
# and calculate:
# Intersection over Union (IoU) 
# Recall 
# Precission
# Misclasssification 

# The Scores are calculated both localy for each inferenced mask and also calculate the mean for the whole dataset 
# 
# both the inputs need to be single channel grayscale. Also, all images needs to be in the same size 
# The Script is written to take the path to the folder with the ground truth images as the first argument and the 
# path to the folder with the inferenced images as the second argument.  
# 
# The Calculations and applications are used to calculate Semantic Segmentation Scores for different networks
# performing inference on forestry imagery. All calculations and technuiqes can be found the in the paper: 
# =diva2%3A1591096&c=1&searchType=SIMPLE&language=sv&query=Filip+Elander&af=%5B%5D&aq=%5B%5B%5D%5D&aq2=%5B%5B%5D%5D&aqe=%5B%5D&noOfRows=50&sortOrder=author_sort_asc&sortOrder2=title_sort_asc&onlyFullText=false&sf=all
# 
# The script will check each image in the dataset. Every pixel in the inferenced mask is check as many times 
# as there are avalible classes in the network. Each class evaluates every pixel in the inferenced mask to see if it belongs 
# to that class or not.  
#   
# Notations
# TP = True positive  --> the class correctly claimed a pixel, mathcing the ground truth    
# FP = False positive --> the class falsy claimed a pixel, miss-mathcing the ground truth 
# TN = True Negative  --> the class correctly rejected a pixel, no deviation from the ground truth 

# The values 0,96,100,150 & 170 are the pixelvalues in the the segmented and ground truth images. 
# Their values also represents segmented classes:
# 0 = Obstacle 
# 96 = Foilage 
# 100 = Sky
# 150 = grass
# 170 = Trail  

############################### USAGE #####################################
# Temrinal arguments: path/to/groundTruthFolder  path/to/inferencedMask 
# Example: IoU.py /Desktop/GroundTruth Desktop/NetworkMask 

#dependencies    
from glob import glob
from PIL import Image 
#import os
#import random
#import argparse
import numpy as np
from pathlib import Path 
import statistics
import sys
  

########################### Holders for Global Variables #######################################

# enable_tot = 1 if the Global mean score is wanted. Else, only the local image scores are calulated 
enable_tot = 1
# GLOBAL dictionary to denote what the pixels are misclassified as if not correctly labeld 
dic_tot = { "0":{"0":0 , "96":0 , "100":0 , "150":0 , "170":0 } ,
        "96":{"0":0 , "96":0 , "100":0 , "150":0 , "170":0 }   ,  
        "100":{"0":0 , "96":0 , "100":0 , "150":0 , "170":0 }    ,
        "150":{"0":0 , "96":0 , "100":0 , "150":0 , "170":0 }   ,
        "170":{"0":0 , "96":0 , "100":0 , "150":0 , "170":0 } } 


# vectors saving the scores from each inference mask 
# JACKARD or IOU = TP / ( TP + FN + FP) -> TP/TOT
# lists to append all the images jackard indexes
jackard_mean = []
jackard_obj = []
jackard_bushes = []
jackard_sky = []
jackard_grass = []
jackard_road = []

# DICE = 2TP / ( 2TP + FN + FP)
dice_mean = []
dice_obj = []
dice_bushes = []
dice_sky = []
dice_grass = []
dice_road = [] 

# Recall TP/TP+FN
recall_mean = []
recall_obj = []
recall_bushes = []
recall_sky = []
recall_grass = []
recall_road = [] 

# precision TP/TP+FP
precision_mean = []
precision_obj = []
precision_bushes = []
precision_sky = []
precision_grass = []
precision_road = [] 


#in_dir = "/Users/filipelander/Desktop/mexkod/input" # GT 
#out_dir = "/Users/filipelander/Desktop/mexkod/output" # segmented image
in_dir = sys.argv[1]  # ground truth dataset
out_dir = sys.argv[2] # segmented image dataset
classes = 5 

# Opens folders
IMAGE_FILES_TRUE = sorted(glob(in_dir + '/*.png'))
IMAGE_FILES_MASK = sorted(glob(out_dir + '/*.png'))


c = 0 
for image_file in IMAGE_FILES_MASK:
    # logic gate to see what classes are represented in ground trhouth, 
    # so not to ruin the iou with a 0% mean value. 
    obj_checker = 0
    bush_checker = 0 
    sky_checker = 0 
    grass_checker = 0 
    road_checker = 0  

    ####################   ERROR CHECKING  ################################

    # manually checking that the correct mask and GT is compared 
    print('-------------------')
    print("image",c)
    print(IMAGE_FILES_TRUE[c])
    print(image_file)
    #image_name =Path(image_file).name 

    # Checking so there are no occurence of pixels that doesn't belong to any of the avalible classes
    im = Image.open(image_file)
    values, counts = np.unique(im, return_counts=True)
    if len(values) >classes:
        print("there are more than",classes,"classes in",image_file)
        print(im.format, im.size, im.mode)
        print(values)
        print(counts)


    ####################  Local scores for every inference mask ################################
        # holder for local misclassification
    dic = { "0":{"0":0 , "96":0 , "100":0 , "150":0 , "170":0 } ,
        "96":{"0":0 , "96":0 , "100":0 , "150":0 , "170":0 }   ,  
        "100":{"0":0 , "96":0 , "100":0 , "150":0 , "170":0 }    ,
        "150":{"0":0 , "96":0 , "100":0 , "150":0 , "170":0 }   ,
        "170":{"0":0 , "96":0 , "100":0 , "150":0 , "170":0 } }  

    mask_arr = np.array(im)
    GT_im = Image.open(IMAGE_FILES_TRUE[c])
    GT_arr = np.array(GT_im)
    X, Y = GT_arr.shape 
    # checking every pixel in the inferenced mask and compares it with its mathcing ground truth pixel 
    for x in range(X):
        for y in range(Y):
            true_pixel = str(GT_arr[x,y])   
            classed_pixel = str(mask_arr[x,y])
            # setting logical gates to see if class exists in local single imafe GT 
            if GT_arr[x,y] == 0:
                obj_checker =1
            if GT_arr[x,y] == 96:
                bush_checker =1 
            if GT_arr[x,y] == 100:
                sky_checker =1 
            if GT_arr[x,y] == 150:
                 grass_checker=1 
            if GT_arr[x,y]== 170:
                road_checker =1 

            try:
                # saving the local classification for single image
                current_val = dic[true_pixel][classed_pixel]
                new_val = current_val + 1 
                dic[true_pixel][classed_pixel] = new_val
                # if global score is requested, accumelate global classification for entire dataset  
                if enable_tot == 1:
                    current_tot = dic_tot[true_pixel][classed_pixel]
                    new_tot_val = current_tot + 1 
                    dic_tot[true_pixel][classed_pixel] = new_tot_val
            except KeyError:
                print("can't find true value:",true_pixel)           
 
    #arrays to keep indexes for the classes 
    dices = []
    ious = []
    recalls = []
    precisions = []

    ########################## Calculating Local scores from the local dictinary with the classification results ################
    if obj_checker ==1:
        obj_TP = dic["0"]["0"]
        obj_FP = dic["96"]["0"] + dic["100"]["0"] + dic["150"]["0"] + dic["170"]["0"] 
        obj_FN = dic["0"]["96"] + dic["0"]["100"] + dic["0"]["150"] + dic["0"]["170"]
        #calc
        iou_obj = obj_TP / (obj_TP + obj_FP + obj_FN)
        dice_im_obj = (2*obj_TP) / ((2*obj_TP) + obj_FP + obj_FN)
       
        try:
            recall_im_obj = obj_TP / (obj_TP + obj_FN)
        except ZeroDivisionError:
            print("there is a zero devision")
            print("TP:",obj_TP)
            print("FN:",obj_FN)
            recall_im_obj = 0 

        try:
            precision_im_obj = obj_TP / (obj_TP + obj_FP)
        except ZeroDivisionError:
            print("there is a zero devision")
            print("TP:",obj_TP)
            print("FP:",obj_FP)
            precision_im_obj = 0 

        # ------------------------- append in local array
        ious.append(iou_obj)
        dices.append(dice_im_obj)
        recalls.append(recall_im_obj)
        precisions.append(precision_im_obj)
        # ------------------------ print
        #print("obj_iou =",iou_obj)
        #print("obj_dice =",dice_im_obj)
        #print("obj_recall =", recall_im_obj)
        #print("obj_precision =", precision_im_obj)
        # ------------------------- append in global array
        jackard_obj.append(iou_obj)
        dice_obj.append(dice_im_obj)
        recall_obj.append(recall_im_obj)
        precision_obj.append(precision_im_obj) 

    if bush_checker ==1:
        bush_TP = dic["96"]["96"]
        bush_FP = dic["0"]["96"] + dic["100"]["96"] + dic["150"]["96"] + dic["170"]["96"] 
        bush_FN = dic["96"]["0"] + dic["96"]["100"] + dic["96"]["150"] + dic["96"]["170"]
        #calc
        iou_bush = bush_TP / (bush_TP + bush_FP + bush_FN)
        dice_im_bush = (2*bush_TP) / ((2*bush_TP) + bush_FP + bush_FN)
        recall_im_bush = bush_TP / ( bush_TP + bush_FN )
        precision_im_bush = bush_TP / ( bush_TP + bush_FP )
        # ------------------------- append in local array
        ious.append(iou_bush)
        dices.append(dice_im_bush)
        recalls.append(recall_im_bush)
        precisions.append(precision_im_bush)
        # ------------------------ print
        # print("bush_iou =",iou_bush)
        # print("bush_dice =",dice_im_bush)
        # print("bush_recall=",recall_im_bush)
        # print("bush_precision=",precision_im_bush)
        # ------------------------- append in global array
        jackard_bushes.append(iou_bush) 
        dice_bushes.append(dice_im_bush)
        recall_bushes.append(recall_im_bush)
        precision_bushes.append(precision_im_bush)   

    if sky_checker ==1:
        sky_TP = dic["100"]["100"]
        sky_FP = dic["0"]["100"] + dic["96"]["100"] + dic["150"]["100"] + dic["170"]["100"] 
        sky_FN = dic["100"]["0"] + dic["100"]["96"] + dic["100"]["150"] + dic["100"]["170"]
        #calc
        iou_sky = sky_TP / (sky_TP + sky_FP + sky_FN)
        dice_im_sky = (2*sky_TP) / ((2*sky_TP) + sky_FP + sky_FN)
        recall_im_sky = sky_TP / (sky_TP + sky_FN)
        precision_im_sky = sky_TP / (sky_TP + sky_FP)
        # ------------------------- append in local array
        ious.append(iou_sky)
        dices.append(dice_im_sky)
        recalls.append(recall_im_sky)
        precisions.append(precision_im_sky)
        # ------------------------ print
        # print("sky_iou =",iou_sky)
        # print("sky_dice =",dice_im_sky)
        # print("sky recall=", recall_im_sky)
        # print("sky precision=", precision_im_sky)
        # ------------------------- append in global array
        jackard_sky.append(iou_sky)   
        dice_sky.append(dice_im_sky)
        recall_sky.append(recall_im_sky)
        precision_sky.append(precision_im_sky)  

    if grass_checker ==1:
        grass_TP = dic["150"]["150"]
        grass_FP = dic["0"]["150"] + dic["96"]["150"] + dic["100"]["150"] + dic["170"]["150"] 
        grass_FN = dic["150"]["0"] + dic["150"]["96"] + dic["150"]["100"] + dic["150"]["170"]
        #calc
        iou_grass = grass_TP / (grass_TP + grass_FP + grass_FN)
        dice_im_grass = (2*grass_TP) / ((2*grass_TP) + grass_FP + grass_FN)
        recall_im_grass = grass_TP / (grass_TP + grass_FN)
        precision_im_grass = grass_TP / (grass_TP + grass_FP)
        # ------------------------- append in local array
        ious.append(iou_grass)
        dices.append(dice_im_grass)
        recalls.append(recall_im_grass)
        precisions.append(precision_im_grass)
        # ------------------------ print
        # print("grass_iou =",iou_grass)
        # print("grass_dice =",dice_im_grass)
        # print("grass_recall=", recall_im_grass)
        # print("grass_precision=", precision_im_grass)
        # ------------------------- append in global array
        dice_grass.append(dice_im_grass)
        jackard_grass.append(iou_grass)
        recall_grass.append(recall_im_grass) 
        precision_grass.append(precision_im_sky) 

    if road_checker ==1:
        road_TP = dic["170"]["170"]
        road_FP = dic["0"]["170"] + dic["96"]["170"] + dic["100"]["170"] + dic["150"]["170"] 
        road_FN = dic["170"]["0"] + dic["170"]["96"] + dic["170"]["100"] + dic["170"]["150"]
        #calc
        iou_road = road_TP / (road_TP + road_FP + road_FN)
        dice_im_road = (2*road_TP) / ((2*road_TP) + road_FP + road_FN)
        recall_im_road = road_TP / (road_TP + road_FN)
        precision_im_road = road_TP / (road_TP + road_FP)
        # ------------------------- append in local array
        ious.append(iou_road)
        dices.append(dice_im_road)
        recalls.append(recall_im_road)
        precisions.append(precision_im_road)
        # ------------------------ print
        # print("road_iou =",iou_road)
        # print("road_dice =",dice_im_road)
        # print("recall road=",recall_im_road)
        # print("precision road=",precision_im_road)
        # ------------------------- append in global array
        dice_road.append(dice_im_road)
        jackard_road.append(iou_road)     
        recall_road.append(recall_im_road)
        precision_road.append(precision_im_road)

    #calculate image indexes 
    single_image_iou = statistics.mean(ious)
    single_image_dice = statistics.mean(dices)
    single_image_recall = statistics.mean(recalls)
    single_image_precision = statistics.mean(precisions)
    #append in global array
    jackard_mean.append(single_image_iou)
    dice_mean.append(single_image_dice)
    recall_mean.append(single_image_recall)
    precision_mean.append(single_image_precision)
    #print("single IoU for image:",image_file, "is", single_image_iou)
    c +=1



 ########################## Calculating Global scores from the global dictinary containing the classifications results ################
print("This values are for CI and Standard deviation")
print("IoU means",jackard_mean)
print("Recall means",recall_mean)
print("Precission means",precision_mean)

print("*************   The result from the vaidation set:   *******************")
if enable_tot == 1:
    #print("stats from tot_dic")
    iou_obj_TP = dic_tot["0"]["0"]
    iou_obj_FP = dic_tot["96"]["0"] + dic["100"]["0"] + dic["150"]["0"] + dic["170"]["0"] 
    iou_obj_FN = dic_tot["0"]["96"] + dic["0"]["100"] + dic["0"]["150"] + dic["0"]["170"]
    iou_obj = iou_obj_TP / (iou_obj_TP + iou_obj_FP + iou_obj_FN)
    #print("IoU for Object class: =",iou_obj)

    iou_bush_TP = dic_tot["96"]["96"]
    iou_bush_FP = dic_tot["0"]["96"] + dic["100"]["96"] + dic["150"]["96"] + dic["170"]["96"] 
    iou_bush_FN = dic_tot["96"]["0"] + dic["96"]["100"] + dic["96"]["150"] + dic["96"]["170"]
    iou_bush = iou_bush_TP / (iou_bush_TP + iou_bush_FP + iou_bush_FN)
    #print("IoU for Bushes class=",iou_bush)

    sky_TP = dic_tot["100"]["100"]
    sky_FP = dic_tot["0"]["100"] + dic["96"]["100"] + dic["150"]["100"] + dic["170"]["100"] 
    sky_FN = dic_tot["100"]["0"] + dic["100"]["96"] + dic["100"]["150"] + dic["100"]["170"]
    iou_sky = sky_TP / (sky_TP + sky_FP + sky_FN)
    #print("IoU for sky class =",iou_sky)

    grass_TP = dic_tot["150"]["150"]
    grass_FP = dic_tot["0"]["150"] + dic["96"]["150"] + dic["100"]["150"] + dic["170"]["150"] 
    grass_FN = dic_tot["150"]["0"] + dic["150"]["96"] + dic["150"]["100"] + dic["150"]["170"]
    iou_grass = grass_TP / (grass_TP + grass_FP + grass_FN)
    #print("IoU for grass class =",iou_grass)

    road_TP = dic_tot["170"]["170"]
    road_FP = dic_tot["0"]["170"] + dic["96"]["170"] + dic["100"]["170"] + dic["150"]["170"] 
    road_FN = dic_tot["170"]["0"] + dic["170"]["96"] + dic["170"]["100"] + dic["170"]["150"]
    iou_road = road_TP / (road_TP + road_FP + road_FN)
    #print("IoU for road class =",iou_road)
    mean_tot_dic = (iou_road + iou_grass + iou_sky + iou_bush + iou_obj) / 5 
    #print("mean IoU tot_dic", mean_tot_dic )

print("the mean from all the single image-class IoU:s")
print("Jackard aka IoU")
print("IoU obj",statistics.mean(jackard_obj)) 
print("IoU bushes", statistics.mean(jackard_bushes))
print("IoU sky", statistics.mean(jackard_sky))
print("IoU grass", statistics.mean(jackard_grass))
print("IoU road", statistics.mean(jackard_road))
arr = np.concatenate((jackard_obj, jackard_bushes,jackard_sky,jackard_grass,jackard_road))
#print(" The mean total IoU of all single Imag total IoU:s ",statistics.mean(jackard_mean))
print("the IoU from all collected IoU:s calculated in the end:  ", statistics.mean(arr))

print("_________")
print("Dice stats")
print("Dice obj",statistics.mean(dice_obj)) 
print("Dice bushes", statistics.mean(dice_bushes))
print("Dice sky", statistics.mean(dice_sky))
print("Dice grass", statistics.mean(dice_grass))
print("Dice road", statistics.mean(dice_road))
#print("mean of images dice ",statistics.mean(dice_mean))
arr = np.concatenate((dice_obj,dice_bushes,dice_sky ,dice_grass ,dice_road))
print("the concatenated Dice", statistics.mean(arr))

print("_________")
print("Recall stats")
print("Recall obj",statistics.mean(recall_obj)) 
print("Recall bushes", statistics.mean(recall_bushes))
print("Recall sky", statistics.mean(recall_sky))
print("Recall grass", statistics.mean(recall_grass))
print("recall road", statistics.mean(recall_road))
#print("mean of images Recall ",statistics.mean(recall_mean))
arr = np.concatenate((recall_obj,recall_bushes,recall_sky ,recall_grass ,recall_road))
print("the concatenated Recall", statistics.mean(arr))

print("_________")
print("Precision stats")
print("Precision obj",statistics.mean(precision_obj)) 
print("Precision bushes", statistics.mean(precision_bushes))
print("Precision sky", statistics.mean(precision_sky))
print("Precision grass", statistics.mean(precision_grass))
print("Precision road", statistics.mean(precision_road))
#print("mean of images Precision ",statistics.mean(precision_mean))
arr = np.concatenate((precision_obj , precision_bushes , precision_sky , precision_grass , precision_road))
print("the concatenated Precision", statistics.mean(arr))

print("-------------------------------------------------")
print("missclassification")
print("what object is classed as:", dic_tot["0"])
print("what Bushes is classed as:", dic_tot["96"])
print("what Sky/background is classed as:", dic_tot["100"])
print("what Grass is classed as:", dic_tot["150"])
print("what Road is classed as:", dic_tot["170"])

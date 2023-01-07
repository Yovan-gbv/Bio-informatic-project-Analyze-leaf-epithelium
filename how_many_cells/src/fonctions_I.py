import skimage
from skimage.morphology import disk
from skimage.measure import label 
from skimage.util import map_array
import tifffile
import napari
import numpy as np
import pandas as pd
import glob
from scipy import ndimage as ndi


# How many cells ?

def segmentation_puzzle(path_img) :
    
    #Read the image 
    img = tifffile.imread(path_img)
    # Put the image in black and white 
    img_gray = skimage.color.rgb2gray(img)

    #Do the median blur
    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)

    # Do the threshold 
    local_threshold = skimage.filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold

    # Remove the small holes 
    mask = skimage.morphology.remove_small_holes(mask.astype(bool), 2500)
    #Remove the small ojects 
    mask = skimage.morphology.remove_small_objects(mask.astype(bool), 500)

    # watershed
    mask_corrected = mask.copy()

    elevation_map_dm = ndi.distance_transform_edt(mask_corrected)

    footprint_size = 150
    coords = skimage.feature.peak_local_max(elevation_map_dm, footprint=np.ones((footprint_size, footprint_size)), labels=mask_corrected)
    mask_seed = np.zeros(elevation_map_dm.shape, dtype=bool)
    mask_seed[tuple(coords.T)] = True
    mask_seed = skimage.morphology.binary_dilation(mask_seed, disk(5))
    markers_dm, _ = ndi.label(mask_seed)
    labels_dm = skimage.segmentation.watershed(-elevation_map_dm, markers_dm, mask=mask_corrected)
    
    return labels_dm
    



def segmentation_longue(path_img) :
    
    #Read the image 
    img = tifffile.imread(path_img)
    # Put the image in black and white 
    img_gray = skimage.color.rgb2gray(img)

    #Do the median blur
    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)

    # Do the threshold 
    local_threshold = skimage.filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold

    # Remove the small holes 
    mask = skimage.morphology.remove_small_holes(mask.astype(bool), 2500)
    #Remove the small ojects 
    mask = skimage.morphology.remove_small_objects(mask.astype(bool), 500)

    # Label
    labelled = skimage.morphology.label(mask)
    
    return labelled



def segmentation_stomates(path_img) :
    
    #Read the image 
    img = tifffile.imread(path_img)
    # Put the image in black and white 
    img_gray = skimage.color.rgb2gray(img)

    #Do the median blur
    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)

    # Do the threshold 
    local_threshold = skimage.filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold

    # Remove the small holes 
    mask = skimage.morphology.remove_small_holes(mask.astype(bool), 2500)
    #Remove the small ojects 
    mask = skimage.morphology.remove_small_objects(mask.astype(bool), 500)

    # Do the erosion of the mask 
    footprint = disk(4)
    mask_eroted = skimage.morphology.binary_erosion(mask, footprint)

    # Label 
    labelled = skimage.morphology.label(mask_eroted)
    
    return labelled


def segmentation_veine(path_img) :
    
    # Read the image
    img = tifffile.imread(path_img)
    # Put the image in black and white 
    img_gray = skimage.color.rgb2gray(img)

    #Do the median blur
    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)

    # Do the threshold 
    local_threshold = skimage.filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold
    
    # Remove the small holes 
    mask = skimage.morphology.remove_small_holes(mask.astype(bool), 2500)
    #Remove the small ojects 
    mask = skimage.morphology.remove_small_objects(mask.astype(bool), 500)
   
    # Do the dilatation of the mask 
    footprint = disk(4)    
    mask_dilation = skimage.morphology.binary_dilation(mask , footprint)
    # Eroted the mask dilated 
    mask_eroted = skimage.morphology.binary_erosion(mask_dilation, footprint)
    #Fill all the holes of the eroted mask 
    mask_fill = ndi.binary_fill_holes(mask_eroted)

    # Label 
    labelled = skimage.morphology.label(mask_fill)
    
    
    return labelled



def segmentation_croco(path_img) :
    
    #Read the image 
    img = tifffile.imread(path_img)
    # Put the image in black and white 
    img_gray = skimage.color.rgb2gray(img)

    #Do the median blur
    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)

    # Do the threshold 
    local_threshold = skimage.filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold

    # Remove the small holes 
    mask = skimage.morphology.remove_small_holes(mask.astype(bool), 2500)
    #Remove the small ojects 
    mask = skimage.morphology.remove_small_objects(mask.astype(bool), 500)
        
    # Do the dilatation of the mask 
    footprint = disk(8)    
    mask_dilation = skimage.morphology.binary_dilation(mask , footprint)
    # Eroted the mask dilated 
    mask_eroted = skimage.morphology.binary_erosion(mask_dilation, footprint)
    #Fill all the holes of the eroted mask 
    mask_fill = ndi.binary_fill_holes(mask_eroted)

    # Label 
    labelled = skimage.morphology.label(mask_fill)
    
    return labelled

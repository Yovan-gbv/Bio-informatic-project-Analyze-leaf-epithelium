from skimage.filters import threshold_yen
from skimage import filters
from skimage import morphology
import skimage
from skimage import data
from skimage.segmentation import clear_border
import napari
import matplotlib.pyplot as plt
from tifffile import imread
import tifffile
from skimage import restoration
import skimage.filters as filters
from skimage.morphology import disk
from scipy import ndimage as ndi
from skimage.segmentation import clear_border
import numpy as np
from skimage import morphology
import napari
from magicgui import magicgui
from napari.types import ImageData, LabelsData
from skimage.feature import peak_local_max
from skimage.measure import label
from skimage.segmentation import watershed
from skimage import measure
import pandas as pd
import glob
from skimage.morphology import skeletonize

def segmentation_puzzle(path_img) :
    
    #Read the image 
    img = imread(path_img)
    # Put the image in black and white 
    img_gray = skimage.color.rgb2gray(img)

    #Do the median blur
    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)

    # Do the threshold 
    local_threshold = filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold

    # Remove the small holes 
    mask = morphology.remove_small_holes(mask.astype(bool), 2500)
    #Remove the small ojects 
    mask = morphology.remove_small_objects(mask.astype(bool), 500)

    # watershed
    mask_corrected = mask.copy()

    elevation_map_dm = ndi.distance_transform_edt(mask_corrected)

    footprint_size = 150
    coords = peak_local_max(elevation_map_dm, footprint=np.ones((footprint_size, footprint_size)), labels=mask_corrected)
    mask_seed = np.zeros(elevation_map_dm.shape, dtype=bool)
    mask_seed[tuple(coords.T)] = True
    mask_seed = morphology.binary_dilation(mask_seed, morphology.disk(5))
    markers_dm, _ = ndi.label(mask_seed)
    labels_dm = watershed(-elevation_map_dm, markers_dm, mask=mask_corrected)
    
    return labels_dm
    



def segmentation_longue(path_img) :
    
    #Read the image 
    img = imread(path_img)
    # Put the image in black and white 
    img_gray = skimage.color.rgb2gray(img)

    #Do the median blur
    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)

    # Do the threshold 
    local_threshold = filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold

    # Remove the small holes 
    mask = morphology.remove_small_holes(mask.astype(bool), 2500)
    #Remove the small ojects 
    mask = morphology.remove_small_objects(mask.astype(bool), 500)

    # Label
    labelled = skimage.morphology.label(mask)
    
    return labelled



def segmentation_stomates(path_img) :
    
    #Read the image 
    img = imread(path_img)
    # Put the image in black and white 
    img_gray = skimage.color.rgb2gray(img)

    #Do the median blur
    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)

    # Do the threshold 
    local_threshold = filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold

    # Remove the small holes 
    mask = morphology.remove_small_holes(mask.astype(bool), 2500)
    #Remove the small ojects 
    mask = morphology.remove_small_objects(mask.astype(bool), 500)

    # Do the erosion of the mask 
    footprint = morphology.disk(4)
    mask_eroted = morphology.binary_erosion(mask, footprint)

    # Label 
    labelled = skimage.morphology.label(mask_eroted)
    
    return labelled


def segmentation_veine(path_img) :
    
    # Read the image
    img = imread(path_img)
    # Put the image in black and white 
    img_gray = skimage.color.rgb2gray(img)

    #Do the median blur
    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)

    # Do the threshold 
    local_threshold = filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold
    
    # Remove the small holes 
    mask = morphology.remove_small_holes(mask.astype(bool), 2500)
    #Remove the small ojects 
    mask = morphology.remove_small_objects(mask.astype(bool), 500)
   
    # Do the dilatation of the mask 
    footprint = morphology.disk(4)    
    mask_dilation = morphology.binary_dilation(mask , footprint)
    # Eroted the mask dilated 
    mask_eroted = morphology.binary_erosion(mask_dilation, footprint)
    #Fill all the holes of the eroted mask 
    mask_fill = ndi.binary_fill_holes(mask_eroted)

    # Label 
    labelled = skimage.morphology.label(mask_fill)
    
    
    return labelled



def segmentation_croco(path_img) :
    
    #Read the image 
    img = imread(path_img)
    # Put the image in black and white 
    img_gray = skimage.color.rgb2gray(img)

    #Do the median blur
    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)

    # Do the threshold 
    local_threshold = filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold

    # Remove the small holes 
    mask = morphology.remove_small_holes(mask.astype(bool), 2500)
    #Remove the small ojects 
    mask = morphology.remove_small_objects(mask.astype(bool), 500)
        
    # Do the dilatation of the mask 
    footprint = morphology.disk(8)    
    mask_dilation = morphology.binary_dilation(mask , footprint)
    # Eroted the mask dilated 
    mask_eroted = morphology.binary_erosion(mask_dilation, footprint)
    #Fill all the holes of the eroted mask 
    mask_fill = ndi.binary_fill_holes(mask_eroted)

    # Label 
    labelled = skimage.morphology.label(mask_fill)
    
    return labelled


def csv_to_df(csv,df):
    #csv need to be a file name bewteen ""
    
    df = pd.read_csv(csv)
    return df


def df_to_csv(df,csv):
    #the csv argument need to be a file name.csv between ""

    df.to_csv(csv, index=False)
    return csv


def sort_df(df):
    
    df = df.sort_values("categories")
    return df


def clean_df(df1,df2,column_name):
    #column_name need to be a name of a column of the dataframe df between ""
    
    df2 = df1.dropna(subset=[column_name]) 
    return df2


def assign_column(df1,df2,column_name):

    df1 = df1.assign(image_name = df2[column_name])
    return df1


def segmentation_puzzle_without_watershed(path_img) :

    img = imread(path_img)
    img_gray = skimage.color.rgb2gray(img)

    #viewer = napari.Viewer()

    #viewer.add_image(img_gray.astype(np.uint8), name = 'astype')
    #viewer.add_image(img_gray*255, name = '255')


    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)


    local_threshold = filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold

    mask = morphology.remove_small_holes(mask.astype(bool), 2500)
    mask = morphology.remove_small_objects(mask.astype(bool), 500)


    #viewer.add_image(mask)
    
    return mask


def segmentation_longue_without_label(path_img) :

    img = imread(path_img)
    img_gray = skimage.color.rgb2gray(img)

    #viewer = napari.Viewer()

    #viewer.add_image(img_gray.astype(np.uint8), name = 'astype')
    #viewer.add_image(img_gray*255, name = '255')


    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)


    local_threshold = filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold

    mask = morphology.remove_small_holes(mask.astype(bool), 2500)
    mask = morphology.remove_small_objects(mask.astype(bool), 500)


    #viewer.add_image(mask)
    
    return mask


def segmentation_stomates_without_label(path_img) :

    img = imread(path_img)
    img_gray = skimage.color.rgb2gray(img)

    #viewer = napari.Viewer()

    #viewer.add_image(img_gray.astype(np.uint8), name = 'astype')
    #viewer.add_image(img_gray*255, name = '255')


    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)


    local_threshold = filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold

    mask = morphology.remove_small_holes(mask.astype(bool), 2500)
    mask = morphology.remove_small_objects(mask.astype(bool), 500)


    #viewer.add_image(mask)
    
    footprint = morphology.disk(4)
    mask_eroted = morphology.binary_erosion(mask, footprint)
    
    return mask_eroted


def segmentation_veine_without_label(path_img) :

    img = imread(path_img)
    img_gray = skimage.color.rgb2gray(img)

    #viewer = napari.Viewer()

    #viewer.add_image(img_gray.astype(np.uint8), name = 'astype')
    #viewer.add_image(img_gray*255, name = '255')


    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)


    local_threshold = filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold

    mask = morphology.remove_small_holes(mask.astype(bool), 2500)
    mask = morphology.remove_small_objects(mask.astype(bool), 500)


    #viewer.add_image(mask)
    
    footprint = morphology.disk(4)    

    mask_dilation = morphology.binary_dilation(mask , footprint)
    mask_eroted = morphology.binary_erosion(mask_dilation, footprint)
    mask_fill = ndi.binary_fill_holes(mask_eroted)

    #viewer.add_image(mask_fill)
    
    return mask_fill


def segmentation_croco_without_label(path_img) :

    img = imread(path_img)
    img_gray = skimage.color.rgb2gray(img)

    #viewer = napari.Viewer()

    #viewer.add_image(img_gray.astype(np.uint8), name = 'astype')
    #viewer.add_image(img_gray*255, name = '255')


    footprint = disk(15.0)
    img_median_blur = skimage.filters.median(img_gray, footprint)


    local_threshold = filters.threshold_local(img_median_blur, block_size=35)
    mask = img_median_blur > local_threshold

    mask = morphology.remove_small_holes(mask.astype(bool), 2500)
    mask = morphology.remove_small_objects(mask.astype(bool), 500)


    #viewer.add_image(mask)
    
    footprint = morphology.disk(8)    

    mask_dilation = morphology.binary_dilation(mask , footprint)
    mask_eroted = morphology.binary_erosion(mask_dilation, footprint)
    mask_fill = ndi.binary_fill_holes(mask_eroted)

    #viewer.add_image(mask_fill)
    
    return mask_fill


#reverse the mask
def inverse_mask(image):
    
    image = ~image #here we reverse the mask by change 0 to 1 and change 1 to 0
    return image


#turn the array in an array with just 0 (if pixel < 3) and 1 (if pixel > 3)
def turn_array_0_1(skeleton):
    
    for pixel in skeleton:
        if pixel.any() < 3:
            pixel == 0
        else:
            pixel == 1
    new_array_TF = skeleton
    
    new_array = new_array_TF.astype(int)
    
    return new_array


def non_triangular_junctions(df_non_triangular_junctions):
    
    #creating a list with all the centroids coordinates:
    centroids = np.array([list(df_non_triangular_junctions['centroid-0']),list(
        df_non_triangular_junctions['centroid-1'])]).T
    
    #find nearest neighbors :

    number = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(centroids)
    distances, indices = number.kneighbors(centroids)

    #determine non triangular junctions :
    non_tri_junctions = np.unique(indices[distances[:, 1] < 5])
    
    #get the centroid coordinates of non triangular junctions :
    df_non_tri_junctions = pd.DataFrame()
    df_non_tri_junctions = df_non_triangular_junctions[df_non_triangular_junctions['label'].isin(non_tri_junctions)]
    
    return (df_non_tri_junctions)
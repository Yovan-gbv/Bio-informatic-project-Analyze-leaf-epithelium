import skimage
from skimage.util import map_array
import tifffile
import napari
import numpy as np
import pandas as pd
import glob
import seaborn as sns

# How can we infer the cell expansions : functions 

def convex_perimeter(regionmask): # get the object mask
    convex_hull = skimage.morphology.convex_hull_image(regionmask) # apply the convex hull to the mask
    perimeter_convex = skimage.measure.perimeter(convex_hull) # find the perimeter of the colonies
    return perimeter_convex


def species(path, specie):
    df_final = pd.DataFrame()
    # I run each image from the species file
    for image in glob.glob(path + '/*.tif'): 
        img = tifffile.imread(image)
        df = pd.DataFrame()
        # I measure the area, perimeter and convex perimeter of the cells in this image
        props = skimage.measure.regionprops_table(     
            img,
            properties=('label', 'area', 'perimeter'),
            extra_properties=(convex_perimeter,)) 
        df = pd.DataFrame(props)
        
        df_final = pd.concat([df_final, df])
    # I create the dataframe with the useful columns (area, species, lobeyness)    
    df_final = df_final.assign(lobeyness = df_final["perimeter"]/df_final["convex_perimeter"])
    df_final["Species_name"]= f'{specie}'
    df_final.reset_index(drop=True)
    
    return df_final


def parametric_map (label_path, df):
    # I open the chosen image with the given informations
    labels_dm = tifffile.imread(label_path)
    # I create the parametric map
    remapped = map_array(
        labels_dm,
        np.array(df['label']),
        np.array(df['lobeyness']),
        )
    # I add the paramtetric map on napari to visualise it
    viewer = napari.Viewer()
    viewer.add_image(remapped, colormap="turbo")
    return

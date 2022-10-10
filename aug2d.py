# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 12:42:56 2022

@author: mrinal
"""
import numpy as np
from scipy.ndimage.interpolation import shift, zoom
from scipy.ndimage import rotate
from skimage import transform

class Augmentor2d():
    """ It performs augmentation on 2D images. It is basically implemented to 
    perform on-the-fly augmentation. So, to implement a custom ImageDataGenerator 
    or any data loader, it will come in handy. It performs following augmentation:
        * Rotation * Flip * Zoom (original image size remains same) 
        * Shift * Rescale * Shear
    """
    

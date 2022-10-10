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
    
    def __init__(self, data):
        
        # If channel axis does not exist, then add it
        if data.ndim == 2: data = np.expand_dims(data, -1)
        
        self.data = data
        
    def rotate(self, angle, mode='constant'):
        return rotate(self.data, angle, mode=mode, reshape=False)
        
    def flip(self, flip_axis):
        '''
        flip_axis = 0 means horizontal flip
        flip_axis = 1 means vertical flip
        '''
        if flip_axis == 0: return np.fliplr(self.data)
        elif flip_axis == 1: return np.flipud(self.data)
        else: raise ValueError('Wrong keyword for flip_axis')
        
    def zoom(self, factor):
        if factor <=1 : # zoom-out            
            zoom_img = zoom(self.data, (factor,factor,1))
        
            start_row = (self.data.shape[0] - zoom_img.shape[0])//2
            start_clm = (self.data.shape[1] - zoom_img.shape[1])//2

            end_row = start_row + zoom_img.shape[0]
            end_clm = start_clm + zoom_img.shape[1]

            padded_zoom_img = np.zeros(self.data.shape, dtype=self.data.dtype)

            padded_zoom_img[start_row:end_row, start_clm:end_clm, ] = zoom_img
            
            return padded_zoom_img
        
        else: # zoom-in
            zoom_img = zoom(self.data, (factor, factor, 1)) 
            
            # Perform center cropping
            c_row, c_clm = zoom_img.shape[0]//2, zoom_img.shape[1]//2

            start_row = c_row - self.data.shape[0]//2
            start_clm = c_clm - self.data.shape[1]//2

            end_row = c_row + (self.data.shape[0] - (c_row - start_row))
            end_clm = c_clm + (self.data.shape[1] - (c_clm - start_clm))

            cropped_zoom_img = zoom_img[start_row:end_row, start_clm:end_clm]
            
            return cropped_zoom_img

    def shift(self, shift_range: tuple=(None, None), mode='constant'):
        'shift_range is a tuple: (shift_h, shift_w). e.g. (5,10)'
        return shift(self.data, (shift_range[0], shift_range[1], 0), mode=mode) # shifted image
    
    def rescale(self, scale_factor):
        return self.data * scale_factor # rescaled image
    
    def shear(self, factor):
        # Transformation matrix
        trans_matrix = transform.AffineTransform(shear=factor)

        shear_img = transform.warp(self.data, inverse_map=trans_matrix) # sheared image
        
        # Image is converted to 0.0 to 1.0. Change to 0 to 255
        shear_img = (shear_img * 255).astype(self.data.dtype)          
        
        return shear_img
    
    

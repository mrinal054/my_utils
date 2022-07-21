# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 22:26:45 2021

@author: mrinal
"""
import numpy as np
import math
from scipy.spatial import distance

#%%
def mcd_gt_to_pred(gt_skl, pred_skl, iso_spacing, high_value=float):
    '''
    This function calculates mean curve distance (MCD) from groundtruth to prediction.
    Inputs:
        - gt_skl: skeletonized ground truth. size: H x W x D
        - pred_skl: skeletonized prediction. size: H x W x D
        - iso_spacing: spacing between two voxels
        - high_value: set MCD to a high value if it fails constraints
    Output:
        - out: returns mcd value 
    '''
    EPSILON = 1e-6
    
    gtCords = np.argwhere(gt_skl == 1)
    n_gt = len(gtCords) # no. of ones in gt
    
    predCords = np.argwhere(pred_skl == 1)
    n_pred = len(predCords)
    
    # Set constraints
    if (n_gt>0 and n_pred==0) or (n_gt==0 and n_pred>0): mcd = high_value # setting a relatively high mcd value
        
    elif n_gt==0 and n_pred == 0: mcd = 0.0
    
    else:
        gtCords_matrix = iso_spacing * gtCords
        predCords_matrix = iso_spacing * predCords

        d = distance.cdist(gtCords_matrix, predCords_matrix, 'euclidean') 

        min_d = np.min(d, axis=1) # find min row-wise
        sum_d = math.fsum(min_d)
        mcd = sum_d/(n_gt + EPSILON)
    return mcd
  
#%%
def mcd_pred_to_gt(gt_skl, pred_skl, iso_spacing, high_value=float):
    '''
    This function calculates mean curve distance (MCD) from prediction to groundtruth.
    Inputs:
        - gt_skl: skeletonized ground truth. size: H x W x D
        - pred_skl: skeletonized prediction. size: H x W x D
        - iso_spacing: spacing between two voxels
        - high_value: set MCD to a high value if it fails constraints
    Output:
        - out: returns mcd value 
    '''    
    EPSILON = 1e-6
    
    gtCords = np.argwhere(gt_skl == 1)
    n_gt = len(gtCords)
    
    predCords = np.argwhere(pred_skl == 1)
    n_pred = len(predCords) # no. of ones in prediction
    
    # Set constraints
    if (n_gt>0 and n_pred==0) or (n_gt==0 and n_pred>0): mcd = high_value # setting a relatively high mcd value
        
    elif n_gt==0 and n_pred == 0: mcd = 0.0
    
    else:    
        gtCord_matrix = iso_spacing * gtCords
        predCord_matrix = iso_spacing * predCords
        
        d = distance.cdist(predCord_matrix, gtCord_matrix, 'euclidean') 
        min_d = np.min(d, axis=1) # find min row-wise
        sum_d = math.fsum(min_d) 
        mcd = sum_d/(n_pred + EPSILON)
    return mcd

  

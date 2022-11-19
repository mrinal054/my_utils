from jenti.patch import Patch
import numpy as np
import random

def choose_fg_idx(
        patch_mask, # an nd-array with size patch_H x patch_W or patch_H x patch_W x patch_Ch
        fg_idx:list, # list of foreground indices. e.g. [2, 4, 7, 9]
        MAX_ROI:bool=True, # if true and the returned patch is a foreground patch, then it
                           # returns the patch that has maximum info or region of interest (roi) 
        ):
  
    """ 
    It is a helper function that picks a foreground index. If MAX_ROI is True,
    then it returns the index of that patch that has max info or roi in it. Otherwise,
    it returns a randomly chosen foreground index.
    
    Return
    --------
    It returns a foreground index. 
    """

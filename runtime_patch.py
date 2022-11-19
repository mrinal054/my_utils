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
    if MAX_ROI: # pick the index of the foreground patch that has maximum roi     
    
        max_nonzeros = 0 # Maximum no. of nonzeros. Initially set it to 0.
        final_fg_idx: int # index of the patch that has maximum roi
        
        for idx in fg_idx:
            
            x = patch_mask[idx] # get the foreground patch mask
            
            n_nonzero = np.count_nonzero(x) # no. of nonzeros in the patch mask
            
            # Compare with current max no. of nonzeros
            if n_nonzero > max_nonzeros: 
                final_fg_idx = idx # update index if new count is higher than the previous count
                max_nonzeros = n_nonzero # update max no. of nonzeros
                
        return final_fg_idx 
        
    else: # randomly pick a foreground index
        return random.choice(fg_idx)
        

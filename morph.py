import numpy as np
from skimage import measure, morphology
from scipy.spatial import distance

#%%
def get_ccomps(vol):
    '''
    This function returns connected component voxel locations
    
    INPUT parameter:
        vol: A 3D/2D binary image
    
    OUTPUT:
        ccomps: A dictonary that holds pixels/voxels' location
        num: no. of connected ccomps
    '''
    labels, num = measure.label(vol, background=0, return_num=True)
    ccomps = {}
    if num > 0:
        for i in range(1,num+1): #iterate over each cccomp
            idx = np.where(labels == i) #find ccomp
            ccomps[i-1] = np.array(idx).T #store row, column, and depth
    else: print('No connected component found')
    
    return ccomps, num

#%%
def get_and_refine_ccomps(vol):
    '''
    This function returns connected component voxel locations. Also, it removes
    any ccomp that has single voxel. 
    
    INPUT parameter:
        vol: A 3D binary image
    
    OUTPUT:
        vol: Refined volume where no single voxel ccomp exist
        ccomps: A dictonary that holds voxels' location
        num: no. of connected ccomps
    '''
    labels, num = measure.label(vol, background=0, return_num=True)
    ccomps = {}
    if num > 0:
        for i in range(1,num+1): #iterate over each cccomp
            idx = np.where(labels == i) #find ccomp
            ccomps[i-1] = np.array(idx).T #store row, column, and depth
    else: print('No connected component found')
    
    # Check all ccomps have at least two voxels. If not then remove it. 
    if num > 0:   
        itr = len(ccomps) # no. of iterations
        for i in range(itr):
            if len(ccomps[i]) < 2:                
                num -= 1 # subtract 1 as this ccomp is deleted
                r,c,d = ccomps[i][0][0], ccomps[i][0][1], ccomps[i][0][2] # row, column, depth of the single voxel
                vol[r,c,d] = 0
                del ccomps[i]
        # Reset keys
        new_keys = np.arange(num)
        old_keys = list(ccomps.keys())
        for i in range(len(ccomps)): ccomps[new_keys[i]] = ccomps.pop(old_keys[i])
    
    return vol, ccomps, num

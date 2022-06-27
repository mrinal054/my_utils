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

#%%
def del_ccomp(vol, connectivity, method, value):
    '''
    This function deletes ccomp which is less than the given size.
    
    INPUT arguments:
        * vol: 3D/2D binary image from which ccomp will be deleted
        * sorted_idx: ccomp volumes will be sorted by their size in descending
        order. So, sorted_idx will be used to get the nth sorted volume.
        * connectivity: In 3D, the connectivity can be either 1, 2 or 3, indicating 6, 18 or 26 neighbors.
            source: https://stackoverflow.com/questions/53089020/what-is-equivalent-to-bwlabeln-with-18-and-26-connected-neighborhood-in-pyth
        * method: two methods - 
            'SizeOfCcomp': if 'value' is 2, then it keeps two largest ccomps
            only
            'NumOfVoxels': if 'value' is 50, then it removes ccomps smaller
            than 50
        * value: assign a value based on which 'method' works
    
    OUTPUT: A 3D/2D image
    '''    
    ccomps, num = get_ccomps(vol)
    vol = vol.astype(bool) # convert to boolean
    if num != 0:
        if method == 'SizeOfCcomp':
            # Get the sizes of ccomps
            sz = [len(ccomps[k]) for k in ccomps.keys()]
            idx = np.argsort(sz) # sorted in ascending order
            idx = idx[::-1] # reversing the order, making it descending
            del_idx = idx[value-1] # subtracting 1, because python starts indexing from 0
            min_allowed_sz = sz[del_idx]
            out = morphology.remove_small_objects(vol, min_size=min_allowed_sz, connectivity=connectivity, in_place=False) 
        elif method == 'NumOfVoxels':
            out = morphology.remove_small_objects(vol, min_size=value, connectivity=connectivity, in_place=False) 
        else:
            raise NameError('Wrong keyword')
    return out.astype('uint8') # converting back to uint8

#%%
def split_vol(vol):
    '''
    This function splits a 3D volume into 2 pieces
    '''
    vol_size = vol.shape
    half_col = np.round(vol_size[1]/2).astype('int16')
    first_half = vol[:,0:half_col,:]
    sec_half = vol[:,half_col:vol_size[1],:]
    return first_half, sec_half

#%%
def merge_vol(first_half, sec_half, vol_size):
    '''
    This function merges two split volumes
    '''
    out = np.zeros(vol_size, dtype='uint8')
    half_col = np.round(vol_size[1]/2).astype('int16')
    out[:,0:half_col,:] = first_half
    out[:,half_col:vol_size[1],:] = sec_half
    return out


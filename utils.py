import numpy as np

#%%
def isNestedList(input):
    '''
    Check if a list is nested or not.
    '''
    # Assert that the input is a list
    assert isinstance(input, list), 'Input is not a list'
    
    # Convert to numpy array
    arr = np.array(input)
    
    return bool(arr.ndim>1)

#%%
def vec2angle(v1, v2, unit='radian'):
    '''
    It calculates angle between two vectors.
    
    Input
    --------
    v1: vector 1. Example: [10, 20, 30]
    v2: vector 2. Example: [30, 20, 40]
    unit: Either radian or degree
    
    Output
    --------
    angle: Angle between two vectors
    
    Example
    --------
    v1 = [10, 20, 10]
    v2 = [20, 40, 30]
    
    angle = vec2angle(v1, v2, unit='degree')

    '''
    unit_v1 = v1 / np.linalg.norm(v1) # unit vector of v1
    unit_v2 = v2 / np.linalg.norm(v2) # unit vector of v2
    dp = np.dot(unit_v1, unit_v2) # dot product
    angle = np.arccos(dp) # calculate inverse cos to get the angle
    
    if unit == 'degree': return np.rad2deg(angle)
    elif unit == 'radian': return angle
    else: print('Wrong keyword for unit')
    
#%%
def points2vec(p1, p2):
    '''
    It calculates the vector from two points.
    
    Input
    -------
    p1: A 2d or 3d point. It is the start point. Example: [20, 30]
    p2: A 2d or 3d point. It is the end point. Example: [20, 30]
    
    Output
    -------
    Output vector in list format.
    
    Example:
    p1 = [10, 20, 10]
    p2 = [20, 40, 30]
    
    vec = points2vec(p1, p2)
    
    '''
    assert len(p1)==len(p2), 'Lenght of two points are not equal'
    
    # If points are in list or tuple, convert to numpy array
    if isinstance(p1, (list, tuple)): p1 = np.array(p1)
    if isinstance(p2, (list, tuple)): p2 = np.array(p2)
        
    return list(p2 - p1)
        
#%%
def sampling(voxels, p1_idx=0, step=5, step_range=(1,5), angle_range=(5,30), rate=0.2, verbose=False):
    '''
    It samples points from a set of points. Step size will be high For points that
    are almost in the same direction. Otherwise, step size will decrease.
    
    Procedure
    -----------
        - Select three points p1, p2, and p3 using the step parameter
        - Calculate two vectors v12 and v13
        - Find angle between v12 and v13
        - Based on the angle, change step size
        
    Input
    -----------
    voxels: list of points. Example: [[x1,y1,z1], [x2,y2,z2], ...]
    p1_idx: index of the first sampleing point
    step: step size
    step_range: min and max allowed value for step size
    angle_range: min and max value of angle. Beyond that, step size will be changed accordingly
    rate: 0.2 means 20% increment or decrement of step size
    verbose: (bool) whether to allow printing
    
    Output
    -----------
    sample_points: a list that contains sampled points
    
    Example:
    -----------
    
    # Read 3d data stored in .mat format
    data = sio.loadmat('s.mat') # contains one canal
    vol = data['cc4'] # get volume
    
    voxels = np.argwhere(vol==1) # get voxels
    voxels = voxels.tolist() # convert to list
    
    sample_points = sampling(voxels, p1_idx=0, step=5, step_range=(1,5), 
                         angle_range=(5,30), rate=0.2, verbose=False)
    '''
    sample_points = []
    
    while(True):
    
        # Ensure limits of step size
        if step > step_range[1]: 
            step = step_range[1]
            if verbose: print('Truncating to max_step')
        
        if step < step_range[0]:
            step = step_range[0]
            if verbose: print('Truncating to min_step')
        
        # Get indices of 2nd and 3rd points
        p2_idx = int(p1_idx + step)
        p3_idx = int(p2_idx + step) 
        
        # Stopping criterion: If p1_idx exceeds range, then append last voxel, and then break 
        if p1_idx >= len(voxels)-1: 
            sample_points.append(voxels[-1])
            if verbose: print('Terminating as p1_idx exceeds range')
            break
        
        # Stopping criterion: If p2_idx exceeds range, then append p1 and last voxel, and then break 
        if p2_idx >= len(voxels)-1: 
            sample_points.append(voxels[p1_idx])
            sample_points.append(voxels[-1])
            if verbose: print('Terminating as p2_idx exceeds range')
            break
        
        # Stopping criterion: If p3_idx exceeds range, then append p1, p2 and last voxel, and then break 
        if p3_idx >= len(voxels)-1: 
            sample_points.append(voxels[p1_idx])
            sample_points.append(voxels[p2_idx])
            sample_points.append(voxels[-1])
            if verbose: print('Terminating as p3_idx exceeds range')
            break
        
        # Calcuate vectors p1p2 and p2p3
        v12 = points2vec(voxels[p1_idx], voxels[p2_idx])
        v23 = points2vec(voxels[p2_idx], voxels[p3_idx])
        
        # Calculate angle between vectors
        angle = vec2angle(v12, v23, unit='degree')
        if verbose: print('Angle: ', angle)
        
        # Redefine step size based on angle
        if angle >= angle_range[0] and angle <= angle_range[1]: 
            if verbose: print('Step size -- no change')
            pass # no need to change step size
        elif angle < angle_range[0]: 
            step = step * (1 + rate) # increase step size
            if verbose: print('Step size -- increased')
        elif angle > angle_range[1]: 
            step = step * (1 - rate) # reduce step size
            if verbose: print('Step size -- decreased')
    #        continue # do this sampling again, no sample will be appended
                
        # Store sample points p1 and p2. Don't need to store p3, it will stored in
        # the next iteration as it will  become p1 then.
        sample_points.append(voxels[p1_idx])
        sample_points.append(voxels[p2_idx])
    #    sample_points.append(voxels[p3_idx])
        
        # Update index of the first point
        p1_idx = p3_idx
        
    return sample_points             
        

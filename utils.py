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
        
        
        

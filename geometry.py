# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 10:24:36 2022

@author: mrinal
    
"""
import numpy as np

def parametricEqu(p1, p2, rng, step):
    t = np.arange(rng[0], rng[1]+step, step)
    x = p1[0] + (p2[0]-p1[0])*t
    y = p1[1] + (p2[1]-p1[1])*t
    
    if len(p1) == 3: # if p1 is a 3D point like (x1, y1, z1)
        z = p1[2] + (p2[2]-p1[2])*t
    
    if len(p1) == 2: # if p1 is a 2D point like (x1, y1)
        return np.transpose([x, y])
    else: # 3D point
        return np.transpose([x, y, z])
    

def line(data, rng, step):
    
    '''
    It uses parametric line euqation. It works for both 2D and 3D lines. 
    
    Input
    -----------
    data: Input array. For 2D line, data.shape=(rows, 2). For 3D array, data.shape=(rows, 3)
    step: Step size
    rng: Range. A tuple, e.g. (start, end) Based on its value, line will be inside of outise the data points.
    
    Output
    -----------
        - Returns line cooridinates
    Example
    -----------
    import numpy as np
    import matplotlib.pyplot as plt
    
    step = 0.01
    rng = (0, 1)
    
    # 2D line
    data2D = np.array([[1, 5], [5, 9]])
    out2D = line(data2D, rng, step)
    
    fig = plt.figure()
    plt.plot(out2D[:,0], out2D[:,1])
    
    # 3D liine
    data3D = np.array([[1, 5, 6], [5, 9, 15]])
    out3D = line(data3D, rng, step)
    
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(out3D[:,0], out3D[:,1], out3D[:,2])
    '''
    
    for i in range(0,data.shape[0]-1):      #if 40 data, then iterates 39 times
        p1 = data[i,:]
        p2 = data[i+1,:]
        p = parametricEqu(p1, p2, rng, step)       #using function
        # Concatenate all points
        if i==0: q = p.copy()
        else: q = np.concatenate((q,p), axis=0)
    return q




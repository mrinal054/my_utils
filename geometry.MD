## Function: line


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


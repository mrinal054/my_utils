import cv2
import os
import matplotlib.pyplot as plt
import numpy as np

dir_src = r'.\test_images'
dir_dst = r'.\test_images_padded'

# Create destination directory if not exists
if not os.path.exists(dir_dst): os.makedirs(dir_dst)

names = os.listdir(dir_src) # read names in the source directory

# Padded image size
frame_size = (512, 512, 3)

for name in names:

    im = cv2.imread(os.path.join(dir_src, name))[:,:,::-1]
    
    pad_row = frame_size[0] - im.shape[0]
    
    pad_coln = frame_size[1] - im.shape[1]
    
    im_pad = np.pad(im, ((0, pad_row), (0, pad_coln), (0, 0)))
    
    """
    (0, pad_row) means no padding above the image and no. of pad_raw below the image.
    
    (0, pad_coln) means no padding on the left of image and no. of pad_coln on the right of the image.
    
    (0, 0) means no padding across the channel axis. 
    """
        
    cv2.imwrite(os.path.join(dir_dst, name), im_pad[:,:,::-1])

    # # Uncomment to visualize
    # fig, ax = plt.subplots(1,2)
    # ax[0].imshow(im)
    # ax[1].imshow(im_pad)
    

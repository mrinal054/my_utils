"""
It calculates accuracy (acc), specificity (sp), precision (p), recall (r), dice score (dice), and intersection-over-union (iou).

Images should be binary or can have two unique values only.

Inputs
------------
    gt: (array: HxWx1 or HxW) Ground truth image which has two unique values only
    pred: (array: HxWx1 or HxW) Predicted image which has two unique values only
    HARD_LINE: (bool) If True, then all metrics are set to 0 when GT is a black image but prediction is not. 

Outputs
------------
    tp, fp, tn, fn, acc, sp, p, r, dice, iou
    
Notes
------------
It considers the following cases - 

    Case I: If there is no GT pixels in the image
        Case I.a: If both GT and prediction are black, then all metrics are set to 100%
        Case I.b: If GT is black, but prediction is not fully black
            If HARD_LINE is True, then set all metrics to 0
            If HARD_LINE is False, then background is considered as y_true, and then metrics are calculated
    Case II: If there is some GT pixels in the image, then it will calculate in the normal way.
             It will consider the foreground as the y_true.     
"""
import numpy as np
from sklearn.metrics import confusion_matrix

def evaluate_binary(gt, pred, HARD_LINE:bool=True):
    
    # Remove single axis
    gt = np.squeeze(gt)
    pred = np.squeeze(pred)

    # Calculate accuracy, specificity, iou, precision, recall, and dice
    flat_mask = np.squeeze(gt).flatten()
    flat_pred = np.squeeze(pred).flatten()

    ep = 1e-6

    # Calculate tp, fp, tn, fn
    unq_mask_val = np.unique(flat_mask) # unique values in the mask. For binary image, it should be 0 and 1
    
    'Case I: If there is no GT pixels in the image'
    if len(unq_mask_val)==1 and unq_mask_val==0: # Only one unique mask value and it is zero
        
        'Case I.a: If both GT and prediction are black' 
        if np.array_equal(flat_mask, flat_pred):
            # Calculate metrics for image-based evaluation. This time consider background as y_true. 
            acc, sp, p, r, dice, iou = 100, 100, 100, 100, 100, 100
                        
            # Calculate the confusion matrix for data-based evaluation
            # Only tn will be counted. All others will be zero. Because the GT and the prediction
            # both have 0 pixels only. So, everything is truly negative.
            tn, fp, fn, tp = len(flat_mask), 0, 0, 0
   
        else:
            'Case I.b: If GT is black, but prediction not'
            if HARD_LINE:
                # If HARD_LINE is True, then all metrics will be set to 0s.
                
                # Calculate metrics for image-based evaluation
                acc, sp, p, r, dice, iou = 0, 0, 0, 0, 0, 0
                
                # Calculate confusion matrix for data-based evaluation
                tp, fn = 0, 0
                fp = np.count_nonzero(flat_pred) # no. of non-zero pixels
                tn = len(flat_pred) - fp # no. of zero intensity pixels
                
            else:
                # If HARD_LINE is False, then metrics will be calculated considering background pixels as y_true.                 
                
                # Calculate metrics for image-based evaluation. 
                # This time consider background as y_true. 
                # Invert (logical NOT) GT and prediction, meaning background will be considered as foreground now.
                invt_flat_mask = np.logical_not(flat_mask) * 1
                invt_flat_pred = np.logical_not(flat_pred) * 1
                
                itn, ifp, ifn, itp = confusion_matrix(invt_flat_mask, invt_flat_pred).ravel()
                
                # Calculate metrics for image-based evaluation 
                acc = ((itp + itn)/(itp + itn + ifn + ifp))*100  
                sp = (itn/(itn + ifp + ep))*100
                p = (itp/(itp + ifp + ep))*100
                r = (itp/(itp + ifn + ep))*100
                dice = 0#(2 * itp / (2 * itp + ifp + ifn))*100
                iou = (itp/(itp + ifp + ifn + ep)) * 100
                
                # Calculate the confusion matrix for data-based evaluation
                # Do not do inversion (logical NOT). There will be some fp and tn. tp and fn will be 0.
                tn, fp, fn, tp = confusion_matrix(flat_mask, flat_pred).ravel()
    
    else:
        'Case II: If there is some GT pixels in the image'
        tn, fp, fn, tp = confusion_matrix(flat_mask, flat_pred).ravel()
        
        # Calculate metrics
        acc = ((tp + tn)/(tp + tn + fn + fp))*100  
        sp = (tn/(tn + fp + ep))*100
        p = (tp/(tp + fp + ep))*100
        r = (tp/(tp + fn + ep))*100
        dice = (2 * tp / (2 * tp + fp + fn))*100
        iou = (tp/(tp + fp + fn + ep)) * 100
    
    return tp, fp, tn, fn, acc, sp, p, r, dice, iou


if __name__ == "__main__":
    import os
    import cv2
    
    # Dataset directory
    dir_gt = r'.\labels'
    dir_pred = r'.\predictions'

    names = os.listdir(dir_gt) # list all image names

    name = names[0] # get one image name

    gt_mask = cv2.imread(os.path.join(dir_gt, name), 0) # read ground truth image

    pred = cv2.imread(os.path.join(dir_pred, name), 0) # read prediction
    
    tp, fp, tn, fn, acc, sp, p, r, dice, iou = evaluate_binary(gt_mask, pred, HARD_LINE=True)


# =============================== End of evaluate_binary =============================== #

# ================================== Start of iouOBB =================================== #
"""
This code calculates IoU between two oriented rectangular bounding boxes.

Author: Mrinal 
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Polygon

def intersection_area(rect1, rect2):
    """Calculate the intersection area between two oriented rectangles."""
    poly1 = Polygon(rect1)
    poly2 = Polygon(rect2)
    if not poly1.intersects(poly2):
        return 0.0

    poly_intersection = poly1.intersection(poly2)
    return poly_intersection.area

def union_area(rect1, rect2):
    """Calculate the union area of two oriented rectangles."""
    poly1 = Polygon(rect1)
    poly2 = Polygon(rect2)
    poly_union = poly1.union(poly2)
    return poly_union.area

def iouOBB(rect1, rect12):
    intersection = intersection_area(rect1, rect2)
    union = union_area(rect1, rect2)
    
    return intersection / union

def plot_oriented_rectangles(rect1, rect2):
    """Plot the two oriented rectangles and their overlapping area."""
    fig, ax = plt.subplots()

    # Plot the first rectangle
    rect1_patch = patches.Polygon(rect1, closed=True, linewidth=1, edgecolor='blue', facecolor='none')
    ax.add_patch(rect1_patch)

    # Plot the second rectangle
    rect2_patch = patches.Polygon(rect2, closed=True, linewidth=1, edgecolor='red', facecolor='none')
    ax.add_patch(rect2_patch)

    # Calculate the overlapping area and plot the overlapping rectangle if it exists
    overlap_area = intersection_area(rect1, rect2)
    if overlap_area > 0:
        intersection_points = np.array(list(Polygon(rect1).intersection(Polygon(rect2)).exterior.coords))
        overlap_patch = patches.Polygon(intersection_points, closed=True, linewidth=1, edgecolor='green', facecolor='none')
        ax.add_patch(overlap_patch)

    ax.set_aspect('equal', 'box')
    ax.autoscale()
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Overlapping Oriented Rectangles')
    plt.grid(True)

    # Create the legend only if there is an overlapping area
    if overlap_area > 0:
        plt.legend([rect1_patch, rect2_patch, overlap_patch], ['Rectangle 1', 'Rectangle 2', 'Overlapping Area'])
    else:
        plt.legend([rect1_patch, rect2_patch], ['Rectangle 1', 'Rectangle 2'])

    plt.show()



if __name__ == "__main__":
    rect1 = [(3, 2), (1, 5), (7, 14), (10, 5)]  # Oriented rectangle 1
    rect2 = [(2, 2), (5, 2), (5, 5), (3, 5)]  # Oriented rectangle 2
    
    print('Intersection: ', intersection_area(rect1, rect2))
    print('Union: ', union_area(rect1, rect2))
    print('IoU: ', iouOBB(rect1, rect2))
    
    plot_oriented_rectangles(rect1, rect2)

# =================================== End of iouOBB =================================== #

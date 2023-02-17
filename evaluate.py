"""
It performs data-based evaluation
"""

import numpy as np
import cv2
from sklearn.metrics import confusion_matrix



def evaluate_binary(gt_mask, pred, HARD_LINE:bool=True):
    
    # Remove single axis
    gt_mask = np.squeeze(gt_mask)
    pred = np.squeeze(pred)

    # Calculate accuracy, specificity, iou, precision, recall, and dice
    flat_mask = np.squeeze(gt_mask).flatten()
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
                # If HARD_LINE is False, then metrics will be calculated considering
                # background pixels as y_true. 
                
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
    
    # Dataset directory
    dir_gt = r'E:\Dataset\wound-segmentation-master\azh_wound_care_center_dataset_patches\test\labels'
    dir_pred = r'F:\Research\Foot_ulcer\predictions\OldDFU\Unet_scse_efficientnet-b7_2023-01-11_00-25-36'

    # FUSeg Dataset
    # dir_label = r'E:\Dataset\wound-segmentation-master\data\Foot Ulcer Segmentation Challenge\Test data FUSeg\fuseg_testting_dataset\test\labels'
    # dir_pred = r'F:\Research\Foot_ulcer\predictions\Unet_scse_efficientnet-b7_2023-01-20_20-13-27_avg'

    names = os.listdir(dir_gt)

    name = names[0]

    gt_mask = cv2.imread(os.path.join(dir_gt, name), 0)

    pred = cv2.imread(os.path.join(dir_pred, name), 0)
    
    tp, fp, tn, fn, acc, sp, p, r, dice, iou = evaluate_binary(gt_mask, pred, HARD_LINE=True)


# my_utils

Currently has - <br>
  * geometry.py <br>
    |-- line: Creates 2D/3D line <br>
  * get.py <br>
    |-- get_dcm: Reads DICOM images <br>
    |-- get_text: Reads text files <br>
    |-- get_dir: Creates directory <br>
    |-- scale_intensity: Clips intensity within a range <br>
    |-- normalize: Normalize data <br>
  * morph.py <br>
    |-- get_ccomps: Returns voxel locations of connected components <br>
    |-- get_and_refine_ccomps: Returns voxel locations of connected components. Also, it removes
    any ccomp that has single voxel. <br>
    |-- del_ccomp: Deletes connected components based on size (slower) <br>
    |-- del_ccomp3d: Deletes connected components based on size (faster) <br>
    |-- split_vol: Splits a 3d volume into two parts <br>
    |-- merge_vol: Merges two volumes <br>
    |-- vol_crop: Crops a specified volume around a given voxel <br>
    
  * utils.py <br>
    |-- vec2angle: Returns angle between two vectors <br>
    |-- points2vec: Calculates the vector from two points <br>
    |-- sampling: Samples data <br>
    |-- isNestedList: Checks if the list is nested <br>
    |-- create_vol: Creates volume based on given voxels and data <br>
    |-- xyz2asc: writes x, y, and z coordinates to a .asc file <br>
  * metrics.py <br>
    |-- mcd_gt_to_pred: Calculates mean curve distance from ground truth to prediction <br>
    |-- mcd_pred_to_gt: Calculates mean curve distance from prediction to ground truth <br>
  * aug2d.py <br>
    |-- Augmentor2d: It performs augmentation on 2D images. [demo](https://github.com/mrinal054/my_utils/blob/main/demo/aug2d/aug2d_demo.ipynb)
  * runtime_patch.py <br>
    |-- It generates on-the-fly patches for PyTorch or TensorFlow DataLoaders. [demo](https://github.com/mrinal054/my_utils/blob/main/demo/runtime_patch/runtime_patch_demo.ipynb) <br>
  * evaluate.py <br>
    |-- evaluate_binary: It calculates accuracy, specificity, precision, recall, dice score, and iou for binary segmentation <br>
    |-- iouOBB: It calculates IoU between two oriented bounding boxes (OBB) <br>
  * crypto.py <br>
    |-- encrypt: It encrypts an image <br>
    <br>
    
   * **Examples** <br>
     |-- image_paddding.py: Padding around an image.
    
  

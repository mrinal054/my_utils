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
    |-- del_ccomp: Deletes connected components based on size <br>
    |-- split_vol: Splits a 3d volume into two parts <br>
    |-- merge_vol: Merges two volumes <br>
    
  * utils.py <br>
    |-- vec2angle: Returns angle between two vectors <br>
    |-- points2vec: Calculates the vector from two points <br>
    |-- sampling: Samples data <br>
    |-- isNestedList: Checks if the list is nested <br>
    |-- create_vol: Creates volume based on given voxels and data
    
   

# -*- coding: utf-8 -*-
import numpy as np
import os
import pydicom

#%% get_dcm
"""
Created on Fri May  7 08:06:50 2021

* 'get_dcm' reads dicom files from a directory
* Input parameter:
    dcm_path: location of dcm data
    
* Output:
    Returns - 
       - dcm_data: dicom data in a single array
       - pix_spacing: spacing of pixel/voxel
       - intensity: min and max intensity

@author: mrinal
"""
# Read dicom
def get_dcm(dcm_path):
    dicom_img = []
    file_names = []
    # Get DICOM image names
    for dir_name, sub_dir_list, file_list in os.walk(dcm_path):
        for file_name in file_list:
            if ".dcm" in file_name.lower():  # check whether the file's DICOM  
                dcm_dir = dir_name
                file_names.append(file_name)
                dicom_img.append(os.path.join(dir_name,file_name))
    
    # Get ref file
    ref = pydicom.dcmread(dicom_img[0])    
    # Get the spacing
    pix_dim = (int(ref.Rows), int(ref.Columns), len(dicom_img))
    # Get spacing values (in mm)
    pix_spacing = (float(ref.PixelSpacing[0]), float(ref.PixelSpacing[1]), float(ref.SliceThickness))    
    # Get the data
    dcm_data = np.zeros(pix_dim, dtype=ref.pixel_array.dtype)   

    # Check if the DICOM file has 'SliceLocation' attribute. It if it has, then store them
    # according to the slice location. Otherwise, store them chronologically. 
    if hasattr(pydicom.dcmread(dicom_img[0]), 'ImagePositionPatient'):               
        # Sort file names according to the slice location
        sliceLocation = [pydicom.dcmread(dicom_img[i]).ImagePositionPatient[-1] for i in range(len(dicom_img))]
        ps = list(np.argsort(sliceLocation)) #ps: position of the sorted slice locations
        ps.reverse() #slices will be sorted in descending order
        sorted_file_names = [file_names[ps[i]] for i in range(len(ps))]
#        print('DICOM sorted by slice location: \n', sorted_file_names)
        print('DICOM sorted by ImagePositionPatient')          
        
        # loop through all the DICOM files
        idx = 0
        for file in sorted_file_names:       
            # read the file
            ds = pydicom.dcmread(os.path.join(dcm_dir,file))
            # store the raw image data
            dcm_data[:, :, idx] = ds.pixel_array
            idx += 1
    else:
        print('No slice location. DICOM sorted chronologically')
#        dicom_img_reverse = dicom_img.copy()
#        dicom_img_reverse.reverse()
        dicom_img.reverse() # slices will be sorted in descending order
        # loop through all the DICOM files
        for file in dicom_img:
            # read the file
            ds = pydicom.dcmread(os.path.join(dcm_dir,file))
            # store the raw image data
            dcm_data[:, :, dicom_img.index(file)] = ds.pixel_array                              
    
    # Get the min and max intensity
    intensity = (dcm_data.min(), dcm_data.max())
        
    return dcm_data, pix_spacing, intensity

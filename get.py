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


#%% get_text
'''
* 'get_text' control points from text files
* In our purpose, we are looking for two text files named - 'iantube_left.asc', 'iantube_right.asc'.
  So, user can change it according to their needs.
* Input parameter:
    text_loc: tentative location of text data

* Output:
    Returns control points in list format
'''
def get_text(text_loc):
    text = []
    for dir_name, sub_dir_list, file_list in os.walk(text_loc):
        for file_name in file_list:
            if ".asc" in file_name.lower():  # check whether the file's DICOM  
                if file_name=='iantube_left.asc'or file_name=='iantube_right.asc':
                    text.append(os.path.join(dir_name,file_name))
    
    if len(text) == 2:
        cp1 = np.loadtxt(text[0]) #left control points
        cp2 = np.loadtxt(text[1]) #right control points
        return list([cp1, cp2]) #returning as a list
    elif len(text) == 1: 
        cp1 = np.loadtxt(text[0]) #left or right control point
        return list(cp1) #returning as a list
    else: raise NameError('Name not found')

#%% get_dir
'''
* This code creates directory
'''
def get_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

#%% Scale intesity within a range
'''
* This code clips intensity within a range.
Example
========
dicom_loc = r'.\dicom'

d, pix_spacing_org, intensity_org = get_dcm(dicom_loc)

min_int, max_int = -1000, 3095 #set min and max intensity level

d_scaled = scale_intensity(d, min_int, max_int)

'''
def scale_intensity(data_set, min_int, max_int):
    # Clip intensity within min intensity to max intensity
    # Clip min intensity
    idx = np.where(data_set <= min_int)
    data_set[idx[0],idx[1],idx[2]] = min_int
    # Clip max intensity
    idx = np.where(data_set >= max_int)
    data_set[idx[0],idx[1],idx[2]] = max_int 
    
    return data_set

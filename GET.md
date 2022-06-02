# Function: get_dcm
---------------------
`get_dcm` reads dicom files from a directory
### Input
- dcm_path: location of dcm data
    
### Output
- Returns - 
   - dcm_data: dicom data in a single array
   - pix_spacing: spacing of pixel/voxel
   - intensity: min and max intensity

### Example
    dcm_loc = r'.\dicom\slc'
    d, pix_spacing_org, intensity_org = get_dcm(dcm_loc)


# Function: scale_intensity
---------------------------------
`scale_intensity` clips intensity within a range.
### Input
- data_set: dicom data
- min_int: Minimum intensity
- max_int: Maximum intensity

### Output
- Returns - 
    - data_set: intensity-scaled data
```
dicom_loc = r'.\dicom'

d, pix_spacing_org, intensity_org = get_dcm(dicom_loc)

min_int, max_int = -1000, 3095 #set min and max intensity level

d_scaled = scale_intensity(d, min_int, max_int)
```

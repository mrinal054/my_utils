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

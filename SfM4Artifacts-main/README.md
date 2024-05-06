
### SfM4Artifacts
## Description
I love history. During my ERASMUS semester at Sapienza University, Italy, I had the opportunity to take classes in classical archeology and computer vision simultaneously. Born out of the passion for archelogy and computer vision, SfM4Artifacts introduces a way to reconstruct 3D models of artifacts using images taken from a mobile device. 

## Example Reconstructions of Roman Artifacts

<img src="https://github.com/ashwin-ned/SfM4Artifacts/blob/main/reconstructed_examples/caracalla.PNG" width="300"/> <img src="https://github.com/ashwin-ned/SfM4Artifacts/blob/main/reconstructed_examples/she_wolf.PNG" width="361"/>

<img src="https://github.com/ashwin-ned/SfM4Artifacts/blob/main/reconstructed_examples/thornboy2.PNG" width="361"/> <img src="https://github.com/ashwin-ned/SfM4Artifacts/blob/main/reconstructed_examples/commodus2.PNG" width="300"/>
<caption>Bust of Caracalla (upper-left); Capitoline Wolf (upper-right); Lo Spinario (lower-left); Bust of Commodus (lower-right).
<br> Capitolini Museum Collections, Rome.</caption>

# Running the code

## Python Version 
run python pipeline.py after setting the image directories and available options. Use "default" when using the included dataset. The ouput folder will contain the final outputs and matched features.
The dense reconstruction and texturing can be done using open source software such as OpenMVS or COLMAP.  
## MATLAB Version
For a simple two view reconstruction using MATLAB use the two_view_SfM.m script. 
Make sure that the camera parameter files are in the same directory oneplus_cameraParameters.mat and oneplus_estimationErrors.mat
Make sure that the directory for the input images are set correctly and exists. 

# Camera Calibration Data

The camera calibration parameters are already provided with the code. The camera used was a mobile camera of a oneplus 6 with 12 MP and 25mm focal length. 
The camera was calibrated using the MATLAB camera calibrator app using 12 different images of a standard camera calibration checkerboard with 20mm squares. The python folder has a text file that contains the information within the MATLAB cameraParameters object.


# Tuning Parameters for better results 

The parameters of the feature detection and matching commands can be tuned for better results i.e. using more octaves, more number of points (selectStrongest) etc. 
MATLAB offers different feature matching algorithms, SURF is used here but others can be used.
Region of Interest can also be used to better detect more features in the object and not the background. 
For the python version, using better feature matching algorithm andaccurate thresholds yeild better results.

# Capturing Datasets

For reconstructing an object, make sure to take pictures of the object with slight overlap between the consecutive images with appropriate lighting and minimum background clutter. The order of the images matter for obtaining the final product. 

Some example datasets captured in Rome is available in the datasets folder.

# Using the Multi-View SfM Script - MATLAB

In the multi_view_SfM folder there are scripts for performing incermental Multi-View SfM using multiple images. The results from this script however, does not restlt in a colored pointcloud. 


# Contact
If you are a museum or art gallery would like to collaborate with me to digitize your exhibits for free, please send me an email at ashwinnedungadi007@gmail.com 

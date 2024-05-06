
% Script for AI LAB: Computer Vision & NLP Project - Two View Sfm
% Author: Ashwin Nedungadi 2035364
% Date: 02/07/2022
% Email: ashwin.nedungadi@tu-dortmund.de

%% Load Data and Camera Parameters

% Load image directory
imageDir = fullfile("C:/Users/Ashwin/Desktop/ERASMUS Semester/AI LAB/Project/Datasets/greek/");

images = imageDatastore(imageDir);

% Adjust the Image Pair Here    
I1 = readimage(images, 1);
I2 = readimage(images, 2);

figure(1)
imshowpair(I1, I2, 'montage'); 
title('Original Images');

% Load camera parameters obtained from calibrator app
paramData = load('oneplus_cameraParameters.mat');
errorData = load('oneplus_estimationErrors.mat');
        
cameraParams = paramData.oneplus_cameraParams
cameraErrors = errorData.oneplus_estimationErrors

% Remove Distortion 
I1 = undistortImage(I1, cameraParams);
I2 = undistortImage(I2, cameraParams);
figure(2)
imshowpair(I1, I2, 'montage');
title('Undistorted Images');


%% Feature Detection & Matching

% Use ROI to cut out the background
roi = [30, 30, size(I1, 2) - 30, size(I1, 1) - 30];

% Detect feature points
% Feature Matcher 1 - Min Eigen Features
%imagePoints1 = detectMinEigenFeatures(im2gray(I1), 'MinQuality', 0.1);

% Feature Matcher 2 - Harris Corner Detector
%imagePoints1 = detectHarrisFeatures(im2gray(I1), "MinQuality", 0.1, 'ROI', roi);

% Feature Matcher 3 - SURF
imagePoints1 = detectSURFFeatures(im2gray(I1), "NumOctaves", 3);


% Visualize detected points
figure(3);
imshow(I1, 'InitialMagnification', 50);
title('100 Strongest Corners from the First Image');
hold on
plot(selectStrongest(imagePoints1, 100));

% Point Trackers
% Create the point tracker
tracker = vision.PointTracker('MaxBidirectionalError', 1, 'NumPyramidLevels', 5);

% Initialize the point tracker
imagePoints1 = imagePoints1.Location;
initialize(tracker, imagePoints1, I1);

% Track the points
[imagePoints2, validIdx] = step(tracker, I2);
matchedPoints1 = imagePoints1(validIdx, :);
matchedPoints2 = imagePoints2(validIdx, :);

% Visualize correspondences
figure(4);
showMatchedFeatures(I1, I2, matchedPoints1, matchedPoints2);
title('Tracked Features');


%% Estimate Essential Matrix

% Estimate the fundamental matrix
[E, epipolarInliers] = estimateEssentialMatrix(matchedPoints1, matchedPoints2, cameraParams, 'Confidence', 99.99);

% Find epipolar inliers
inlierPoints1 = matchedPoints1(epipolarInliers, :);
inlierPoints2 = matchedPoints2(epipolarInliers, :);

% Display inlier matches
figure(5);
showMatchedFeatures(I1, I2, inlierPoints1, inlierPoints2);
title('Epipolar Inliers');

%% Compute Camera Pose

[orient, loc] = relativeCameraPose(E, cameraParams, inlierPoints1, inlierPoints2);

%% 3D Recontruction from Matched Points

% Detect dense feature points. Use an ROI to exclude border points
roi = [30, 30, size(I1, 2) - 30, size(I1, 1) - 30];
imagePoints1 = detectMinEigenFeatures(im2gray(I1), 'ROI', roi, ...
    'MinQuality', 0.001);

% Create the point tracker
tracker = vision.PointTracker('MaxBidirectionalError', 1, 'NumPyramidLevels', 5);

% Initialize the point tracker
imagePoints1 = imagePoints1.Location;
initialize(tracker, imagePoints1, I1);

% Track the points
[imagePoints2, validIdx] = step(tracker, I2);
matchedPoints1 = imagePoints1(validIdx, :);
matchedPoints2 = imagePoints2(validIdx, :);

% Compute the camera matrices for each position of the camera
tform1 = rigid3d;
camMatrix1 = cameraMatrix(cameraParams, tform1);

% Compute extrinsics of the second camera
cameraPose = rigid3d(orient, loc);
tform2 = cameraPoseToExtrinsics(cameraPose);
camMatrix2 = cameraMatrix(cameraParams, tform2);

% Compute the 3-D points
points3D = triangulate(matchedPoints1, matchedPoints2, camMatrix1, camMatrix2);

% Get the color of each reconstructed point
numPixels = size(I1, 1) * size(I1, 2);
allColors = reshape(I1, [numPixels, 3]);
colorIdx = sub2ind([size(I1, 1), size(I1, 2)], round(matchedPoints1(:,2)), ...
    round(matchedPoints1(:, 1)));
color = allColors(colorIdx, :);

% Create the point cloud
ptCloud = pointCloud(points3D, 'Color', color);


%% Visualize Pointcloud
% Visualize the camera locations and orientations
cameraSize = 0.3;
figure(6)
plotCamera('Size', cameraSize, 'Color', 'r', 'Label', '1', 'Opacity', 0);
hold on
grid on
plotCamera('Location', loc, 'Orientation', orient, 'Size', cameraSize, 'Color', 'b', 'Label', '2', 'Opacity', 0);

% Visualize the point cloud
pcshow(ptCloud, 'VerticalAxis', 'y', 'VerticalAxisDir', 'down', 'MarkerSize', 45);

% Rotate and zoom the plot
camorbit(0, -30);
camzoom(1.5);

% Label the axes
xlabel('x-axis');
ylabel('y-axis');
zlabel('z-axis')

title('Up to Scale Reconstruction of the Scene');

%% Save Pointcloud

pcwrite(ptCloud,'output.ply','Encoding','ascii');



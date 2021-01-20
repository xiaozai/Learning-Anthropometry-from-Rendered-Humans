clear ; close all ;clc;

I = imread('bg05.jpg');
% imshow(I)

% Performs the 2D convolution
for i = 1:3
    I(:, :, i) = uint8(conv2(I(:, :, i), ones(20)/20^2, 'same'));
end

% figure(); imshow(I);

imwrite(I, 'bg05_blur.jpg');


%%
clear ; close all; clc;

kernelSize = 11;
kernel = ones(kernelSize) / kernelSize.^2;

imgList = dir('img/*.jpg');
    
for idx = 1:50
    imgName = imgList(idx).name;
    I = imread(['img/' imgName]);
    blurryImage = imfilter(I, kernel, 'replicate');
    imwrite(blurryImage, ['blur_img/' imgName])
end

% I = imread('bg05.jpg');
% imshow(I)
% figure(); imshow(blurryImage)

%%
clear ; close all; clc;

imgList = dir('img/*.jpg');

for idx = 1:50
   imgName = imgList(idx).name;
   I = imread(['img/' imgName]);
   
   rz_I = imresize(I,[640 640], 'bilinear');
   
   imwrite(rz_I, ['rz_img/' imgName]);
end
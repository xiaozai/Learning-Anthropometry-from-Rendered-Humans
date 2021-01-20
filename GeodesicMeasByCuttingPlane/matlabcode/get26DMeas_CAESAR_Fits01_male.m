clear; close all; clc;

% bodyPartTris
load('bodyParts-SMPL/bodyPartTris.mat');
% landmarksIdx
load('geodesicLandmarks-SMPL/26D-Meas-Landmarks-Idx.mat');

meshDir = '/home/yans/Pre-Process-CAESARfits/CAESAR-Fits01/';
pcaDir  = '20D-PCA';
gender  = 'male';

objInDir   = [meshDir gender '-fits-nicp/'];
measOutDir = [meshDir gender '-geodesic-meas/'];

meas_26D_dir  = [measOutDir '26D-Meas/'];
label_26D_dir = [measOutDir '26D-Meas-Labels/'];
insectPts_dir = [measOutDir '26D-Meas-insectPts/'];

sampleList = dir([objInDir '*.obj']);
nSamples = length(sampleList);

for ii =1:nSamples
   sname = sampleList(ii).name(1:end-4);
   [verts, ~] = loadObj([objInDir sname '.obj']);
   [meas_26D, insectPts_26D] = getMeas26D(verts, landmarksIdx, bodyPartTris);
   
   save([meas_26D_dir sname '.mat'], 'meas_26D');
   save([insectPts_dir sname '.mat'], 'insectPts_26D');
   
   y = zeros(1,26);
   y(1)  = meas_26D.circ_01;
   y(2)  = meas_26D.circ_02;
   y(3)  = meas_26D.circ_03;
   y(4)  = meas_26D.circ_04;
   y(5)  = meas_26D.circ_05;
   y(6)  = meas_26D.circ_06;
   y(7)  = meas_26D.circ_07;
   y(8)  = (meas_26D.circ_08_left + meas_26D.circ_08_right) / 2;
   y(9)  = (meas_26D.circ_09_left + meas_26D.circ_09_right) / 2;
   y(10) = (meas_26D.circ_10_left + meas_26D.circ_10_right) / 2;
   y(11) = (meas_26D.circ_11_left + meas_26D.circ_11_right) / 2;
   y(12) = (meas_26D.circ_12_left + meas_26D.circ_12_right) / 2;
   y(13) = (meas_26D.circ_13_left + meas_26D.circ_13_right) / 2;
   y(14) = (meas_26D.circ_14_left + meas_26D.circ_14_right) / 2;
   y(15) = (meas_26D.circ_15_left + meas_26D.circ_15_right) / 2;
   
   y(16) = meas_26D.circ_16;
   y(17) = meas_26D.circ_17;
   y(18) = meas_26D.circ_18;
   y(19) = meas_26D.circ_19;
   y(20) = meas_26D.circ_20;
   
   y(21) = (meas_26D.circ_21_left + meas_26D.circ_21_right) / 2;
   y(22) = (meas_26D.circ_22_left + meas_26D.circ_22_right) / 2;
   y(23) = (meas_26D.circ_23_left + meas_26D.circ_23_right) / 2;
   y(24) = (meas_26D.circ_24_left + meas_26D.circ_24_right) / 2;
   y(25) = (meas_26D.circ_25_left + meas_26D.circ_25_right) / 2;
   y(26) = (meas_26D.circ_26_left + meas_26D.circ_26_right) / 2;
   
   save([label_26D_dir sname '.mat'], 'y');
end




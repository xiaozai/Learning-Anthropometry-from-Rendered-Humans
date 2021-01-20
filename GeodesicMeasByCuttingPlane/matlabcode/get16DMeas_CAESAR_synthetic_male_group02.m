clear;close all; clc;

load('../bodyParts-SMPL/bodyPartTris.mat');

load('../geodesicLandmarks-SMPL/16D-Meas-Landmarks-Idx.mat');

% meshDir = '/home/yan/Data2/narvi_folder/Pre-Process-CAESARfits/CAESAR-Fits01/';
% % meshDir = '/home/yans/Pre-Process-CAESARfits/CAESAR-Fits01/';
pcaDir  = '20D-PCA';
gender  = 'male';

in_mesh_dir  = [meshDir gender '-synthetic-samples/' pcaDir '/' 'obj/'];
out_meas_dir = [meshDir gender '-synthetic-samples/' pcaDir '/' 'meas/'];

groupIdx = 2;
groupDir = sprintf('group%02d', groupIdx);

objInDir   = [in_mesh_dir groupDir '/']; 
measOutDir = [out_meas_dir groupDir '/'];

meas_16D_dir  = [measOutDir '16D-Meas/'];
label_16D_dir = [measOutDir '16D-Meas-Labels/'];
insectPts_dir = [measOutDir '16D-Meas-insectPts/'];

sampleList = dir([objInDir '*.obj']);
nSamples = length(sampleList);

for ii =1:nSamples
   sname = sampleList(ii).name(1:end-4);
   [verts, ~] = loadObj([objInDir sname '.obj']);
   [meas_16D, insectPts_16D] = getMeas16D(verts, landmarksIdx, bodyPartTris);
   
%    visualize16DMeas(verts, landmarksIdx, insectPts_16D);
   
   save([meas_16D_dir sname '.mat'], 'meas_16D');
   save([insectPts_dir sname '.mat'], 'insectPts_16D');
   
   y = zeros(1,16);
   y(1)  = meas_16D.A;
   y(2)  = meas_16D.B;
   y(3)  = meas_16D.C;
   y(4)  = meas_16D.D;
   y(5)  = meas_16D.E;
   y(6)  = meas_16D.F;
   y(7)  = meas_16D.G;
   y(8)  = meas_16D.H;
   y(9)  = meas_16D.I;
   y(10) = meas_16D.J;
   y(11) = meas_16D.K;
   y(12) = meas_16D.L;
   y(13) = meas_16D.M;
   y(14) = meas_16D.N;
   y(15) = meas_16D.O;
   y(16) = meas_16D.P;
   
   save([label_16D_dir sname '.mat'], 'y');
end




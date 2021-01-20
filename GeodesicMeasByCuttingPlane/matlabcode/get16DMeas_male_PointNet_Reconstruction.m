clear; close all; clc;

load('../bodyParts-SMPL/bodyPartTris.mat'); % bodyPartTris
load('../geodesicLandmarks-SMPL/16D-Meas-Landmarks-Idx.mat'); % landmarksIdx

measOutDir = '/home/yan/Data2/narvi_folder/HKS-Net/exp/female_HKS_6890V_TOP/reconstruct_meas/';
label_16D_dir = [measOutDir '16D-Meas-Labels/'];
insectPts_dir = [measOutDir '16D-Meas-insectPts/'];

objInDir = '/home/yan/Data2/narvi_folder/HKS-Net/exp/female_HKS_6890V_TOP/reconstruct_mesh/';
sampleList = dir([objInDir '*.obj']);
nSamples = length(sampleList);

for ii =1:nSamples
   sname = sampleList(ii).name(1:end-4);
   [verts, ~] = loadObj([objInDir sname '.obj']);
   [meas_16D, insectPts_16D] = getMeas16D(verts, landmarksIdx, bodyPartTris);
   
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




% compare the mean dist err between Registered Mesh and Optimized Mesh

clear; close all; clc;

% loadObj function
addpath('/home/yan/Data2/3D_Body_Reconstruction/Code/RegistrationProcess/NonRigid_ICP/');  

OriMeshDir = '/home/yan/Data2/3D_Body_Reconstruction/Dataset/scans/NOMO3D_Dataset2/male/';
RegMeshDir = '/home/yan/Data2/3D_Body_Reconstruction/Dataset/scans/NonRigidICP_Registered_NOMO3D_Dataset1/male/';

OptMeshDir = '/home/yan/Data2/3D_Body_Reconstruction/Dataset/scans/Optimized_Registered_NOMO3D_Dataset1/Original_A_Posed/male04/';


meshList = dir([OptMeshDir '*.obj']);  % 179 samples

% reg_ori_Dist = 0;
% opt_ori_Dist = 0;
reg_opt_Dist = 0;

for idx = 1:length(meshList)
    meshName = meshList(idx).name;
    
%     [oriV, ~] = loadObj([OriMeshDir meshName]);
    [regV, ~] = loadObj([RegMeshDir meshName]);
    [optV, ~] = loadObj([OptMeshDir meshName]);
    
    % compare the mean distance
    
    % dist between regV and oriV
    % find the closest points in oriV for regV, calculate the distance
%     [~, d] = dsearchn(oriV, regV);
%     reg_ori_Dist = reg_ori_Dist + mean(d);
%     % dist between optV and oriV
%     [~, d] = dsearchn(oriV, optV);
%     opt_ori_Dist = opt_ori_Dist + mean(d);
    % dist between regV and optV
    reg_opt_Dist = reg_opt_Dist + mean(sqrt(sum((regV - optV).^2, 2)));
    
    if mod(idx, 20) == 0
        disp(idx)
    end
end

% reg_ori_Dist = reg_ori_Dist / length(meshList);
% opt_ori_Dist = opt_ori_Dist / length(meshList);
reg_opt_Dist = reg_opt_Dist / length(meshList);
% Non Rigid ICP Registration Process
% 2018.01.19, Song Yan

clear; close all; clc;
%--------------------------------------------------------------------------
Options.gamm = 1;
Options.epsilon = 1e-4;
Options.maxIter = 500;
Options.alphaSet = linspace(100, 1, 100);

data_folder = '/home/yan/Data2/NOMO_Project_P1/data/';
% out_folder = [data_folder 'registered_mesh/female_nonrigidICP_boarder/'];
out_folder = '/home/yan/Data2/NOMO_Project_P2/Methods/ObjectiveFunctionOptimization/NonRigidICP_Registration/NOMO3D_Dataset2/male/';

%--------------------------------------------------------------------------
% use the same initial template
source_obj = [data_folder 'smpl_mesh/init_template_male.obj'];
[source.vertices, source.faces] = loadObj(source_obj);

targetList = dir('/home/yan/Data2/NOMO_Project_P2/Dataset/NOMO3D_Dataset2/scans/male/*.obj');
targetNum = size(targetList, 1);
%--------------------------------------------------------------------------
% disp(['Non-Rigid ICP starts : ' datestr(datetime('now'))]);
% 
for idx = 1:targetNum
    obj_name = targetList(idx).name;
    target_obj = ['/home/yan/Data2/NOMO_Project_P2/Dataset/NOMO3D_Dataset2/scans/male/' obj_name];
    out_mesh = [out_folder obj_name];
    
    [target.vertices, target.faces] = loadObj(target_obj);
    NonRigid_ICP(source, target, out_mesh, Options);
    
    if mod(idx, 10) == 0
        disp( [num2str(idx) ' of ' num2str(targetNum) ' samples done']);
    end
end
% 
% disp(['Non-Rigid ICP done : ' datestr(datetime('now'))]);





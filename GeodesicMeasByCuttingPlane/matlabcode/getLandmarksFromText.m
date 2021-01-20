clear; close all; clc;

landmarkDir = 'geodesicLandmarks-SMPL/16D-Meas/';

% on the upper torso and head 
A_idx = readVidText([landmarkDir 'A_head_circ.txt']);
A_idx = A_idx + 1; % matlab starts from 1

B_idx = readVidText([landmarkDir 'B_neck_circ.txt']);
B_idx = B_idx + 1; % matlab starts from 1

D_idx = readVidText([landmarkDir 'D_chest_circ.txt']);
D_idx = D_idx + 1; % matlab starts from 1

E_idx = readVidText([landmarkDir 'E_waist_circ.txt']);
E_idx = E_idx + 1; % matlab starts from 1

F_idx = readVidText([landmarkDir 'F_pelvis_circ.txt']);
F_idx = F_idx + 1; % matlab starts from 1

% on the arm, left and right
G_idx_left = readVidText([landmarkDir 'G_wrist_circ_left.txt']);
G_idx_left = G_idx_left + 1; % matlab starts from 1

G_idx_right = readVidText([landmarkDir 'G_wrist_circ_right.txt']);
G_idx_right = G_idx_right + 1; % matlab starts from 1

H_idx_left = readVidText([landmarkDir 'H_bicep_circ_left.txt']);
H_idx_left = H_idx_left + 1; % matlab starts from 1

H_idx_right = readVidText([landmarkDir 'H_bicep_circ_right.txt']);
H_idx_right = H_idx_right + 1; % matlab starts from 1

I_idx_left = readVidText([landmarkDir 'I_forearm_circ_left.txt']);
I_idx_left = I_idx_left + 1; % matlab starts from 1

I_idx_right = readVidText([landmarkDir 'I_forearm_circ_right.txt']);
I_idx_right = I_idx_right + 1; % matlab starts from 1

L_idx_left = readVidText([landmarkDir 'L_thigh_circ_left.txt']);
L_idx_left = L_idx_left + 1; % matlab starts from 1

L_idx_right = readVidText([landmarkDir 'L_thigh_circ_right.txt']);
L_idx_right = L_idx_right + 1; % matlab starts from 1

M_idx_left = readVidText([landmarkDir 'M_calf_circ_left.txt']);
M_idx_left = M_idx_left + 1; % matlab starts from 1

M_idx_right = readVidText([landmarkDir 'M_calf_circ_right.txt']);
M_idx_right = M_idx_right + 1; % matlab starts from 1

N_idx_left = readVidText([landmarkDir 'N_ankle_circ_left.txt']);
N_idx_left = N_idx_left + 1; % matlab starts from 1

N_idx_right = readVidText([landmarkDir 'N_ankle_circ_right.txt']);
N_idx_right = N_idx_right + 1; % matlab starts from 1

% straight line
J_idx_left = readVidText([landmarkDir 'J_arm_len_left.txt']);
J_idx_left = J_idx_left + 1; % matlab starts from 1

J_idx_right = readVidText([landmarkDir 'J_arm_len_right.txt']);
J_idx_right = J_idx_right + 1; % matlab starts from 1

K_idx_left = readVidText([landmarkDir 'K_leg_len_left.txt']);
K_idx_left = K_idx_left + 1; % matlab starts from 1

K_idx_right = readVidText([landmarkDir 'K_leg_len_right.txt']);
K_idx_right = K_idx_right + 1; % matlab starts from 1

C_idx = readVidText([landmarkDir 'C_crotch_len.txt']);
C_idx = C_idx + 1; % matlab starts from 1

P_idx = readVidText([landmarkDir 'P_shoulder_breadth.txt']);
P_idx = P_idx + 1; % matlab starts from 1

% Head top
O_idx = readVidText([landmarkDir 'O_overall_height.txt']);
O_idx = O_idx + 1; % matlab starts from 1

landmarksIdx = struct();
landmarksIdx.A_idx = A_idx;
landmarksIdx.B_idx = B_idx;
landmarksIdx.C_idx = C_idx;
landmarksIdx.D_idx = D_idx;
landmarksIdx.E_idx = E_idx;
landmarksIdx.F_idx = F_idx;
landmarksIdx.G_idx_left  = G_idx_left;
landmarksIdx.G_idx_right = G_idx_right;
landmarksIdx.H_idx_left  = H_idx_left;
landmarksIdx.H_idx_right = H_idx_right;
landmarksIdx.I_idx_left  = I_idx_left;
landmarksIdx.I_idx_right = I_idx_right;
landmarksIdx.J_idx_left  = J_idx_left;
landmarksIdx.J_idx_right = J_idx_right;
landmarksIdx.K_idx_left  = K_idx_left;
landmarksIdx.K_idx_right = K_idx_right;
landmarksIdx.L_idx_left  = L_idx_left;
landmarksIdx.L_idx_right = L_idx_right;
landmarksIdx.M_idx_left  = M_idx_left;
landmarksIdx.M_idx_right = M_idx_right;
landmarksIdx.N_idx_left  = N_idx_left;
landmarksIdx.N_idx_right = N_idx_right;
landmarksIdx.O_idx = O_idx;
landmarksIdx.P_idx = P_idx;

save('geodesicLandmarks-SMPL/16D-Meas-Landmarks-Idx.mat', 'landmarksIdx');

%%
clear; close all; clc;
landmarkDir = '../geodesicLandmarks-SMPL/27D-Meas/';

idx01 = readVidText([landmarkDir '1_head_circ.txt']);
idx01 = idx01 + 1; % matlab starts from 1

idx02 = readVidText([landmarkDir '2_neck_circ.txt']);
idx02 = idx02 + 1; % matlab starts from 1

idx03 = readVidText([landmarkDir '3_chest_circ.txt']);
idx03 = idx03 + 1; % matlab starts from 1

idx04 = readVidText([landmarkDir '4_underBust_circ.txt']);
idx04 = idx04 + 1; % matlab starts from 1

idx05 = readVidText([landmarkDir '5_maxWaist_circ.txt']);
idx05 = idx05 + 1; % matlab starts from 1

idx06 = readVidText([landmarkDir '6_trouserWaist_circ.txt']);
idx06 = idx06 + 1; % matlab starts from 1

idx07 = readVidText([landmarkDir '7_pelvis_circ.txt']);
idx07 = idx07 + 1; % matlab starts from 1

idx08_left = readVidText([landmarkDir '8_thigh_circ_left.txt']);
idx08_left = idx08_left + 1; % matlab starts from 1

idx08_right = readVidText([landmarkDir '8_thigh_circ_right.txt']);
idx08_right = idx08_right + 1; % matlab starts from 1

idx09_left = readVidText([landmarkDir '9_knee_circ_left.txt']);
idx09_left = idx09_left + 1; % matlab starts from 1

idx09_right = readVidText([landmarkDir '9_knee_circ_right.txt']);
idx09_right = idx09_right + 1; % matlab starts from 1

idx10_left = readVidText([landmarkDir '10_calf_circ_left.txt']);
idx10_left = idx10_left + 1; % matlab starts from 1

idx10_right = readVidText([landmarkDir '10_calf_circ_right.txt']);
idx10_right = idx10_right + 1; % matlab starts from 1

idx11_left = readVidText([landmarkDir '11_ankle_circ_left.txt']);
idx11_left = idx11_left + 1; % matlab starts from 1

idx11_right = readVidText([landmarkDir '11_ankle_circ_right.txt']);
idx11_right = idx11_right + 1; % matlab starts from 1

idx12_left = readVidText([landmarkDir '12_bicep_circ_left.txt']);
idx12_left = idx12_left + 1; % matlab starts from 1

idx12_right = readVidText([landmarkDir '12_bicep_circ_right.txt']);
idx12_right = idx12_right + 1; % matlab starts from 1

idx13_left = readVidText([landmarkDir '13_elbow_circ_left.txt']);
idx13_left = idx13_left + 1; % matlab starts from 1

idx13_right = readVidText([landmarkDir '13_elbow_circ_right.txt']);
idx13_right = idx13_right + 1; % matlab starts from 1

idx14_left = readVidText([landmarkDir '14_forearm_circ_left.txt']);
idx14_left = idx14_left + 1; % matlab starts from 1

idx14_right = readVidText([landmarkDir '14_forearm_circ_right.txt']);
idx14_right = idx14_right + 1; % matlab starts from 1

idx15_left = readVidText([landmarkDir '15_wrist_circ_left.txt']);
idx15_left = idx15_left + 1; % matlab starts from 1

idx15_right = readVidText([landmarkDir '15_wrist_circ_right.txt']);
idx15_right = idx15_right + 1; % matlab starts from 1

idx16 = readVidText([landmarkDir '16_head_len.txt']);
idx16 = idx16 + 1; % matlab starts from 1

idx17 = readVidText([landmarkDir '17_neck_len.txt']);
idx17 = idx17 + 1; % matlab starts from 1

idx18 = readVidText([landmarkDir '18_shoulder_breadth.txt']);
idx18 = idx18 + 1; % matlab starts from 1

idx19 = readVidText([landmarkDir '19_upperTorso_len.txt']);
idx19 = idx19 + 1; % matlab starts from 1

idx20 = readVidText([landmarkDir '20_pelvis_len.txt']);
idx20 = idx20 + 1; % matlab starts from 1

idx21_left = readVidText([landmarkDir '21_upperLeg_len_left.txt']);
idx21_left = idx21_left + 1; % matlab starts from 1

idx21_right = readVidText([landmarkDir '21_upperLeg_len_right.txt']);
idx21_right = idx21_right + 1; % matlab starts from 1

idx22_left = readVidText([landmarkDir '22_lowerLeg_len_left.txt']);
idx22_left = idx22_left + 1; % matlab starts from 1

idx22_right = readVidText([landmarkDir '22_lowerLeg_len_right.txt']);
idx22_right = idx22_right + 1; % matlab starts from 1

idx23_left = readVidText([landmarkDir '23_upperArm_len_left.txt']);
idx23_left = idx23_left + 1; % matlab starts from 1

idx23_right = readVidText([landmarkDir '23_upperArm_len_right.txt']);
idx23_right = idx23_right + 1; % matlab starts from 1

idx24_left = readVidText([landmarkDir '24_lowerArm_len_left.txt']);
idx24_left = idx24_left + 1; % matlab starts from 1

idx24_right = readVidText([landmarkDir '24_lowerArm_len_right.txt']);
idx24_right = idx24_right + 1; % matlab starts from 1

idx25_left = readVidText([landmarkDir '25_hand_len_left.txt']);
idx25_left = idx25_left + 1; % matlab starts from 1

idx25_right = readVidText([landmarkDir '25_hand_len_right.txt']);
idx25_right = idx25_right + 1; % matlab starts from 1

idx26_left = readVidText([landmarkDir '26_foot_len_left.txt']);
idx26_left = idx26_left + 1; % matlab starts from 1

idx26_right = readVidText([landmarkDir '26_foot_len_right.txt']);
idx26_right = idx26_right + 1; % matlab starts from 1

idx27_left = readVidText([landmarkDir '27_crotchToFloor_len_left.txt']);
idx27_left = idx27_left + 1; % matlab starts from 1

idx27_right = readVidText([landmarkDir '27_crotchToFloor_len_right.txt']);
idx27_right = idx27_right + 1; % matlab starts from 1


landmarksIdx = struct();
landmarksIdx.idx01 = idx01;
landmarksIdx.idx02 = idx02;
landmarksIdx.idx03 = idx03;
landmarksIdx.idx04 = idx04;
landmarksIdx.idx05 = idx05;
landmarksIdx.idx06 = idx06;
landmarksIdx.idx07 = idx07;
landmarksIdx.idx08_left  = idx08_left;
landmarksIdx.idx08_right = idx08_right;
landmarksIdx.idx09_left  = idx09_left;
landmarksIdx.idx09_right = idx09_right;
landmarksIdx.idx10_left  = idx10_left;
landmarksIdx.idx10_right = idx10_right;
landmarksIdx.idx11_left  = idx11_left;
landmarksIdx.idx11_right = idx11_right;
landmarksIdx.idx12_left  = idx12_left;
landmarksIdx.idx12_right = idx12_right;
landmarksIdx.idx13_left  = idx13_left;
landmarksIdx.idx13_right = idx13_right;
landmarksIdx.idx14_left  = idx14_left;
landmarksIdx.idx14_right = idx14_right;
landmarksIdx.idx15_left  = idx15_left;
landmarksIdx.idx15_right = idx15_right;
landmarksIdx.idx16 = idx16;
landmarksIdx.idx17 = idx17;
landmarksIdx.idx18 = idx18;
landmarksIdx.idx19 = idx19;
landmarksIdx.idx20 = idx20;
landmarksIdx.idx21_left  = idx21_left;
landmarksIdx.idx21_right = idx21_right;
landmarksIdx.idx22_left  = idx22_left;
landmarksIdx.idx22_right = idx22_right;
landmarksIdx.idx23_left  = idx23_left;
landmarksIdx.idx23_right = idx23_right;
landmarksIdx.idx24_left  = idx24_left;
landmarksIdx.idx24_right = idx24_right;
landmarksIdx.idx25_left  = idx25_left;
landmarksIdx.idx25_right = idx25_right;
landmarksIdx.idx26_left  = idx26_left;
landmarksIdx.idx26_right = idx26_right;
landmarksIdx.idx27_left  = idx27_left;
landmarksIdx.idx27_right = idx27_right;

save('../geodesicLandmarks-SMPL/27D-Meas-Landmarks-Idx.mat', 'landmarksIdx');


function [meas, insectPts] = getMeas16D(verts, landmarkIdx, bodyPartTris)
    % 1) an ellipse, using geodesic distance between a few points
    % A head circ, B neck circ,D chest circ, E waist circ, F pelvis circ, 
    [A_circ, A_instPt] = getMeasByCuttingPlane(verts, landmarkIdx.A_idx, bodyPartTris.head_tris, true); % using horizontal plane
    [B_circ, B_instPt] = getMeasByCuttingPlane(verts, landmarkIdx.B_idx, bodyPartTris.neck_tris, false); 
    [D_circ, D_instPt] = getMeasByCuttingPlane(verts, landmarkIdx.D_idx, bodyPartTris.upperTorso_tris, true); % using horizontal plane
    [E_circ, E_instPt] = getMeasByCuttingPlane(verts, landmarkIdx.E_idx, bodyPartTris.upperTorso_tris, true); % using horizontal plane
    [F_circ, F_instPt] = getMeasByCuttingPlane(verts, landmarkIdx.F_idx, bodyPartTris.upperTorso_tris, true); % using horizontal plane
    % G wrist circ, 
    [G_circ_left,  G_instPt_left]  = getMeasByCuttingPlane(verts, landmarkIdx.G_idx_left,  bodyPartTris.leftArm_tris);
    [G_circ_right, G_instPt_right] = getMeasByCuttingPlane(verts, landmarkIdx.G_idx_right, bodyPartTris.rightArm_tris);
    G_circ = (G_circ_left + G_circ_right) / 2;
    % H bicep circ
    [H_circ_left,  H_instPt_left]  = getMeasByCuttingPlane(verts, landmarkIdx.H_idx_left,  bodyPartTris.leftArm_tris);
    [H_circ_right, H_instPt_right] = getMeasByCuttingPlane(verts, landmarkIdx.H_idx_right, bodyPartTris.rightArm_tris);
    H_circ = (H_circ_left + H_circ_right)/2;
    % I forearm circ,
    [I_circ_left,  I_instPt_left]  = getMeasByCuttingPlane(verts, landmarkIdx.I_idx_left,  bodyPartTris.leftArm_tris);
    [I_circ_right, I_instPt_right] = getMeasByCuttingPlane(verts, landmarkIdx.I_idx_right, bodyPartTris.rightArm_tris);
    I_circ = (I_circ_left + I_circ_right) / 2;
    % L thigh circ,
    [L_circ_left,  L_instPt_left]  = getMeasByCuttingPlane(verts, landmarkIdx.L_idx_left,  bodyPartTris.leftLeg_tris, true);  % using horizontal plane
    [L_circ_right, L_instPt_right] = getMeasByCuttingPlane(verts, landmarkIdx.L_idx_right, bodyPartTris.rightLeg_tris, true); % using horizontal plane
    L_circ = (L_circ_left + L_circ_right) / 2;
    % M calf circ, left and right
    [M_circ_left,  M_instPt_left]  = getMeasByCuttingPlane(verts, landmarkIdx.M_idx_left,  bodyPartTris.leftLeg_tris, true);  % using horizontal plane
    [M_circ_right, M_instPt_right] = getMeasByCuttingPlane(verts, landmarkIdx.M_idx_right, bodyPartTris.rightLeg_tris, true); % using horizontal plane
    M_circ = (M_circ_left + M_circ_right) / 2;
    % N ankle circ, left and right
    [N_circ_left,  N_instPt_left]  = getMeasByCuttingPlane(verts, landmarkIdx.N_idx_left,  bodyPartTris.leftLeg_tris, true);  % using horizontal plane
    [N_circ_right, N_instPt_right] = getMeasByCuttingPlane(verts, landmarkIdx.N_idx_right, bodyPartTris.rightLeg_tris, true); % using horizontal plane
    N_circ = (N_circ_left + N_circ_right) / 2;
    
    % 2) Straight line measurements
    % C crotch length, the vertical distance y-axis
    C_len = abs(verts(landmarkIdx.C_idx(1), 2) - verts(landmarkIdx.C_idx(2), 2));
    % O overall height, the vertical height y-axis
    O_height = abs(max(verts(:,2)) - min(verts(:,2)));
    % J_arm_len, the Euclidean distances
    J_len_left  = sqrt(sum((verts(landmarkIdx.J_idx_left(1), :)  - verts(landmarkIdx.J_idx_left(2), :)).^2));
    J_len_right = sqrt(sum((verts(landmarkIdx.J_idx_right(1), :) - verts(landmarkIdx.J_idx_right(2), :)).^2));
    J_len = (J_len_left + J_len_right) / 2;
    % K leg Len, the Euclidean distances
    K_len_left  = sqrt(sum((verts(landmarkIdx.K_idx_left(1), :)  - verts(landmarkIdx.K_idx_left(2), :)).^2));
    K_len_right = sqrt(sum((verts(landmarkIdx.K_idx_right(1), :) - verts(landmarkIdx.K_idx_right(2), :)).^2));
    K_len = (K_len_left + K_len_right) / 2;
    % P shoulder Breadth, the Euclidean distances
    P_len = sqrt(sum((verts(landmarkIdx.P_idx(1),:) - verts(landmarkIdx.P_idx(2), :)).^2));
    %----------------------------------------------------------------------
    meas = struct();
    
    meas.A = A_circ;
    meas.B = B_circ;
    meas.C = C_len;
    meas.D = D_circ;
    meas.E = E_circ;
    meas.F = F_circ;
    meas.G = G_circ;
    meas.H = H_circ;
    meas.I = I_circ;
    meas.J = J_len;
    meas.K = K_len;
    meas.L = L_circ;
    meas.M = M_circ;
    meas.N = N_circ;
    meas.O = O_height;
    meas.P = P_len;
    
    insectPts = struct();
    
    insectPts.A = A_instPt;
    insectPts.B = B_instPt;
    insectPts.D = D_instPt;
    insectPts.E = E_instPt;
    insectPts.F = F_instPt;
    insectPts.G_left  = G_instPt_left;
    insectPts.G_right = G_instPt_right;
    insectPts.H_left  = H_instPt_left;
    insectPts.H_right = H_instPt_right;
    insectPts.I_left  = I_instPt_left;
    insectPts.I_right = I_instPt_right;
    insectPts.L_left  = L_instPt_left;
    insectPts.L_right = L_instPt_right;
    insectPts.M_left  = M_instPt_left;
    insectPts.M_right = M_instPt_right;
    insectPts.N_left  = N_instPt_left;
    insectPts.N_right = N_instPt_right;
end
function [meas, insectPts] = getMeas27D(verts, landmarkIdx, bodyPartTris)
    % 1) an ellipse, using geodesic distance between a few points
    % 
    [circ_01, insectPt_01] = getMeasByCuttingPlane(verts, landmarkIdx.idx01, bodyPartTris.head_tris, true);       % 01 head circ, using horizontal plane
    [circ_02, insectPt_02] = getMeasByCuttingPlane(verts, landmarkIdx.idx02, bodyPartTris.neck_tris);             % 02 neck circ, 
    [circ_03, insectPt_03] = getMeasByCuttingPlane(verts, landmarkIdx.idx03, bodyPartTris.upperTorso_tris, true); % 03 chest circ, using horizontal plane
    [circ_04, insectPt_04] = getMeasByCuttingPlane(verts, landmarkIdx.idx04, bodyPartTris.upperTorso_tris, true); % 04 underBust circ, using horizontal plane
    [circ_05, insectPt_05] = getMeasByCuttingPlane(verts, landmarkIdx.idx05, bodyPartTris.upperTorso_tris, true); % 05 maxWaist circ, using horizontal plane
    [circ_06, insectPt_06] = getMeasByCuttingPlane(verts, landmarkIdx.idx06, bodyPartTris.upperTorso_tris, true); % 06 trouserWaist circ, using horizontal plane
    [circ_07, insectPt_07] = getMeasByCuttingPlane(verts, landmarkIdx.idx07, bodyPartTris.upperTorso_tris, true); % 07 pelvis circ, using horizontal plane

    [circ_08_left,  insectPt_08_left]  = getMeasByCuttingPlane(verts, landmarkIdx.idx08_left,  bodyPartTris.leftLeg_tris,  true); % thigh left circ, using horizontal plane
    [circ_08_right, insectPt_08_right] = getMeasByCuttingPlane(verts, landmarkIdx.idx08_right, bodyPartTris.rightLeg_tris, true); % thigh right circ, using horizontal plane
   
    [circ_09_left,  insectPt_09_left]  = getMeasByCuttingPlane(verts, landmarkIdx.idx09_left,  bodyPartTris.leftLeg_tris,  true); % knee left circ, using horizontal plane
    [circ_09_right, insectPt_09_right] = getMeasByCuttingPlane(verts, landmarkIdx.idx09_right, bodyPartTris.rightLeg_tris, true); % knee right circ, using horizontal plane
    
    [circ_10_left,  insectPt_10_left]  = getMeasByCuttingPlane(verts, landmarkIdx.idx10_left,  bodyPartTris.leftLeg_tris,  true); % calf left circ, using horizontal plane
    [circ_10_right, insectPt_10_right] = getMeasByCuttingPlane(verts, landmarkIdx.idx10_right, bodyPartTris.rightLeg_tris, true); % calf right circ, using horizontal plane
    
    [circ_11_left,  insectPt_11_left]  = getMeasByCuttingPlane(verts, landmarkIdx.idx11_left,  bodyPartTris.leftLeg_tris,  true); % ankle left circ, using horizontal plane
    [circ_11_right, insectPt_11_right] = getMeasByCuttingPlane(verts, landmarkIdx.idx11_right, bodyPartTris.rightLeg_tris, true); % ankle right circ, using horizontal plane
    
    [circ_12_left,  insectPt_12_left]  = getMeasByCuttingPlane(verts, landmarkIdx.idx12_left,  bodyPartTris.leftArm_tris);  % bicep left circ, 
    [circ_12_right, insectPt_12_right] = getMeasByCuttingPlane(verts, landmarkIdx.idx12_right, bodyPartTris.rightArm_tris); % bicep right circ, 
    
    [circ_13_left,  insectPt_13_left]  = getMeasByCuttingPlane(verts, landmarkIdx.idx13_left,  bodyPartTris.leftArm_tris);  % elbow left circ,
    [circ_13_right, insectPt_13_right] = getMeasByCuttingPlane(verts, landmarkIdx.idx13_right, bodyPartTris.rightArm_tris); % elbow right circ,
    
    [circ_14_left,  insectPt_14_left]  = getMeasByCuttingPlane(verts, landmarkIdx.idx14_left,  bodyPartTris.leftArm_tris);  % forearm left circ,
    [circ_14_right, insectPt_14_right] = getMeasByCuttingPlane(verts, landmarkIdx.idx14_right, bodyPartTris.rightArm_tris); % forearm right circ,
    
    [circ_15_left,  insectPt_15_left]  = getMeasByCuttingPlane(verts, landmarkIdx.idx15_left,  bodyPartTris.leftArm_tris);  % wrist left circ,
    [circ_15_right, insectPt_15_right] = getMeasByCuttingPlane(verts, landmarkIdx.idx15_right, bodyPartTris.rightArm_tris); % wrist right circ,
    
    % 2) Straight line measurements
    %  the vertical distance y-axis
    len_16 = abs(verts(landmarkIdx.idx16(1), 2) - verts(landmarkIdx.idx16(2), 2)); % 16 head len,
    len_17 = abs(verts(landmarkIdx.idx17(1), 2) - verts(landmarkIdx.idx17(2), 2)); % 17 neck len,  
    len_19 = abs(verts(landmarkIdx.idx19(1), 2) - verts(landmarkIdx.idx19(2), 2)); % 19 upperTorso len,
    len_20 = abs(verts(landmarkIdx.idx20(1), 2) - verts(landmarkIdx.idx20(2), 2)); % 20 pelvis len,  
    
    
    % the Euclidean distances
    len_18       = sqrt(sum((verts(landmarkIdx.idx18(1),:)       - verts(landmarkIdx.idx18(2), :)).^2));       % 18 shoulder breadth,
    len_21_left  = sqrt(sum((verts(landmarkIdx.idx21_left(1),:)  - verts(landmarkIdx.idx21_left(2), :)).^2));  % 21 upperLeg Len left
    len_21_right = sqrt(sum((verts(landmarkIdx.idx21_right(1),:) - verts(landmarkIdx.idx21_right(2), :)).^2)); % 21 upperLeg Len righ
    len_22_left  = sqrt(sum((verts(landmarkIdx.idx22_left(1),:)  - verts(landmarkIdx.idx22_left(2), :)).^2));  % 22 lowerLeg Len left
    len_22_right = sqrt(sum((verts(landmarkIdx.idx22_right(1),:) - verts(landmarkIdx.idx22_right(2), :)).^2)); % 22 lowerLeg Len right
    len_23_left  = sqrt(sum((verts(landmarkIdx.idx23_left(1),:)  - verts(landmarkIdx.idx23_left(2), :)).^2));  % 23 upper_arm len left
    len_23_right = sqrt(sum((verts(landmarkIdx.idx23_right(1),:) - verts(landmarkIdx.idx23_right(2), :)).^2)); % 23 upper_arm len right
    len_24_left  = sqrt(sum((verts(landmarkIdx.idx24_left(1),:)  - verts(landmarkIdx.idx24_left(2), :)).^2));  % 24 lower arm len left
    len_24_right = sqrt(sum((verts(landmarkIdx.idx24_right(1),:) - verts(landmarkIdx.idx24_right(2), :)).^2)); % 24 lower arm len right
    len_25_left  = sqrt(sum((verts(landmarkIdx.idx25_left(1),:)  - verts(landmarkIdx.idx25_left(2), :)).^2));  % 25 hand len left
    len_25_right = sqrt(sum((verts(landmarkIdx.idx25_right(1),:) - verts(landmarkIdx.idx25_right(2), :)).^2));
    len_26_left  = sqrt(sum((verts(landmarkIdx.idx26_left(1),:)  - verts(landmarkIdx.idx26_left(2), :)).^2));  % 26 foot len left
    len_26_right = sqrt(sum((verts(landmarkIdx.idx26_right(1),:) - verts(landmarkIdx.idx26_right(2), :)).^2));
    len_27_left  = sqrt(sum((verts(landmarkIdx.idx27_left(1),:)  - verts(landmarkIdx.idx27_left(2), :)).^2));  % 27 Crotch To Floor len left
    len_27_right = sqrt(sum((verts(landmarkIdx.idx27_right(1),:) - verts(landmarkIdx.idx27_right(2), :)).^2));
    
    % O overall height, the vertical height y-axis
    O_height = abs(max(verts(:,2)) - min(verts(:,2)));
    %----------------------------------------------------------------------
    meas = struct();
    
    meas.circ_01 = circ_01;
    meas.circ_02 = circ_02;
    meas.circ_03 = circ_03;
    meas.circ_04 = circ_04;
    meas.circ_05 = circ_05;
    meas.circ_06 = circ_06;
    meas.circ_07 = circ_07;
    
    meas.circ_08_left  = circ_08_left;
    meas.circ_08_right = circ_08_right;
    
    meas.circ_09_left  = circ_09_left;
    meas.circ_09_right = circ_09_right;
    
    meas.circ_10_left  = circ_10_left;
    meas.circ_10_right = circ_10_right;
    
    meas.circ_11_left  = circ_11_left;
    meas.circ_11_right = circ_11_right;
    
    meas.circ_12_left  = circ_12_left;
    meas.circ_12_right = circ_12_right;
    
    meas.circ_13_left  = circ_13_left;
    meas.circ_13_right = circ_13_right;
    
    meas.circ_14_left  = circ_14_left;
    meas.circ_14_right = circ_14_right;
    
    meas.circ_15_left  = circ_15_left;
    meas.circ_15_right = circ_15_right;
    
    meas.circ_16 = len_16;
    meas.circ_17 = len_17;
    meas.circ_18 = len_18;
    meas.circ_19 = len_19;
    meas.circ_20 = len_20;
    
    meas.circ_21_left  = len_21_left;
    meas.circ_21_right = len_21_right;
    
    meas.circ_22_left  = len_22_left;
    meas.circ_22_right = len_22_right;
    
    meas.circ_23_left  = len_23_left;
    meas.circ_23_right = len_23_right;
    
    meas.circ_24_left  = len_24_left;
    meas.circ_24_right = len_24_right;
    
    meas.circ_25_left  = len_25_left;
    meas.circ_25_right = len_25_right;
   
    meas.circ_26_left  = len_26_left;
    meas.circ_26_right = len_26_right;
    
    meas.circ_27_left  = len_27_left;
    meas.circ_27_right = len_27_right;
    
    meas.O_height = O_height;
    
    insectPts = struct();
    
    insectPts.insectPt_01 = insectPt_01;
    insectPts.insectPt_02 = insectPt_02;
    insectPts.insectPt_03 = insectPt_03;
    insectPts.insectPt_04 = insectPt_04;
    insectPts.insectPt_05 = insectPt_05;
    insectPts.insectPt_06 = insectPt_06;
    insectPts.insectPt_07 = insectPt_07;
    
    insectPts.insectPt_08_left  = insectPt_08_left;
    insectPts.insectPt_08_right = insectPt_08_right;
    
    insectPts.insectPt_09_left  = insectPt_09_left;
    insectPts.insectPt_09_right = insectPt_09_right;
    
    insectPts.insectPt_10_left  = insectPt_10_left;
    insectPts.insectPt_10_right = insectPt_10_right;
    
    insectPts.insectPt_11_left  = insectPt_11_left;
    insectPts.insectPt_11_right = insectPt_11_right;
    
    insectPts.insectPt_12_left  = insectPt_12_left;
    insectPts.insectPt_12_right = insectPt_12_right;
    
    insectPts.insectPt_13_left  = insectPt_13_left;
    insectPts.insectPt_13_right = insectPt_13_right;
    
    insectPts.insectPt_14_left  = insectPt_14_left;
    insectPts.insectPt_14_right = insectPt_14_right;
    
    insectPts.insectPt_15_left  = insectPt_15_left;
    insectPts.insectPt_15_right = insectPt_15_right;
    
end

% To save .obj file
% 2018.01.19, Song Yan
%
% input:  file_path, vertices, faces, colorV = None
% 
function saveObj_with16DMeasLine(out_path, vertices, faces, insectPts)
    [numVerts, ~] = size(vertices);
    
    fid = fopen(out_path, 'w');
    for v_id = 1:numVerts
        v = vertices(v_id, :);
        fprintf(fid, 'v %f %f %f\n', v);
    end
    
    [numVertsA, ~] = size(insectPts.A);
    [numVertsB, ~] = size(insectPts.B);
    [numVertsD, ~] = size(insectPts.D);
    [numVertsE, ~] = size(insectPts.E);
    [numVertsF, ~] = size(insectPts.F);
    [numVertsG_left, ~] = size(insectPts.G_left);
    [numVertsG_right, ~] = size(insectPts.G_right);
    [numVertsH_left, ~] = size(insectPts.H_left);
    [numVertsH_right, ~] = size(insectPts.H_right);
    [numVertsI_left, ~] = size(insectPts.I_left);
    [numVertsI_right, ~] = size(insectPts.I_right);
    [numVertsL_left, ~] = size(insectPts.L_left);
    [numVertsL_right, ~] = size(insectPts.L_right);
    [numVertsM_left, ~] = size(insectPts.M_left);
    [numVertsM_right, ~] = size(insectPts.M_right);
    [numVertsN_left, ~] = size(insectPts.N_left);
    [numVertsN_right, ~] = size(insectPts.N_right);
    
    writePointsToFile(fid, insectPts.A);
    writePointsToFile(fid, insectPts.B);
    writePointsToFile(fid, insectPts.D);
    writePointsToFile(fid, insectPts.E);
    writePointsToFile(fid, insectPts.F);
    writePointsToFile(fid, insectPts.G_left);
    writePointsToFile(fid, insectPts.G_right);
    writePointsToFile(fid, insectPts.H_left);
    writePointsToFile(fid, insectPts.H_right);
    writePointsToFile(fid, insectPts.I_left);
    writePointsToFile(fid, insectPts.I_right);
    writePointsToFile(fid, insectPts.L_left);
    writePointsToFile(fid, insectPts.L_right);
    writePointsToFile(fid, insectPts.M_left);
    writePointsToFile(fid, insectPts.M_right);
    writePointsToFile(fid, insectPts.N_left);
    writePointsToFile(fid, insectPts.N_right);
    
    for f_id = 1:length(faces)
        fprintf(fid, 'f %d %d %d\n', faces(f_id, :));
    end
    
    lineIdx = numVerts+1:numVerts+numVertsA;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsA;
    
    lineIdx = numVerts+1:numVerts+numVertsB;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsB;
    
    lineIdx = numVerts+1:numVerts+numVertsD;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsD;
    
    lineIdx = numVerts+1:numVerts+numVertsE;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsE;
    
    lineIdx = numVerts+1:numVerts+numVertsF;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsF;
    
    lineIdx = numVerts+1:numVerts+numVertsG_left;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsG_left;
    
    lineIdx = numVerts+1:numVerts+numVertsG_right;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsG_right;
    
    lineIdx = numVerts+1:numVerts+numVertsH_left;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsH_left;
    
    lineIdx = numVerts+1:numVerts+numVertsH_right;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsH_right;
    
    lineIdx = numVerts+1:numVerts+numVertsI_left;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsI_left;
    
    lineIdx = numVerts+1:numVerts+numVertsI_right;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsI_right;
    
    lineIdx = numVerts+1:numVerts+numVertsL_left;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsL_left;
    
    lineIdx = numVerts+1:numVerts+numVertsL_right;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsL_right;
    
    lineIdx = numVerts+1:numVerts+numVertsM_left;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsM_left;
    
    lineIdx = numVerts+1:numVerts+numVertsM_right;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsM_right;
    
    lineIdx = numVerts+1:numVerts+numVertsN_left;
    writeLineToFile(fid, lineIdx)
    numVerts = numVerts+numVertsN_left;
    
    lineIdx = numVerts+1:numVerts+numVertsN_right;
    writeLineToFile(fid, lineIdx)
%     numVerts = numVerts+numVertsN_right;
    
    fclose(fid);
end

function writePointsToFile(fid, pts)
    [numExtras, ~] = size(pts);
    for vid = 1:numExtras
        v = pts(vid, :);
        fprintf(fid, 'v %f %f %f 255 0 0\n', v);
    end
end

function writeLineToFile(fid, lineIdx)
    fprintf(fid, 'l');
    for ii = 1:length(lineIdx)
       fprintf(fid, ' %d', lineIdx(ii)); 
    end
    fprintf(fid, '\n');
end
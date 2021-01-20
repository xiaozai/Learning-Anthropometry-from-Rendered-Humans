function meas = getMeas27D_extra(verts, landmarkIdx)
    len_27_left  = sqrt(sum((verts(landmarkIdx.idx27_left(1),:)  - verts(landmarkIdx.idx27_left(2), :)).^2));  % 27 Crotch To Floor len left
    len_27_right = sqrt(sum((verts(landmarkIdx.idx27_right(1),:) - verts(landmarkIdx.idx27_right(2), :)).^2));
    
    meas = struct();
    meas.circ_27_left  = len_27_left;
    meas.circ_27_right = len_27_right;
    
end

function [m, pts] = getMeasByCuttingPlane(verts, vertIdx, tris, horizontal)
    pt01 = verts(vertIdx(1), :);
    pt02 = verts(vertIdx(2), :);
    pt03 = verts(vertIdx(3), :);
    
    if nargin == 3
        horizontal = false;
    end
    
    if horizontal
        n = [0, 1, 0];
        p = pt01;
    else
        n = cross(pt01 - pt02, pt01 - pt03);
        p = (pt01 + pt02 + pt03)/3;
    end

    pts = getInsectPoints(verts, tris, n, p, false);
    m   = sum(sqrt(sum(((pts(1:end-1, :) - pts(2:end, :)).^2), 2)));
end
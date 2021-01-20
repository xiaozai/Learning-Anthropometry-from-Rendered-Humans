function visualize16DMeas(verts, landmarksIdx, insectPts)
    minY = min(verts(:,2));
    maxY = max(verts(:,2));
    minX = min(verts(:,1));
    maxX = max(verts(:,1));
    maxZ = max(verts(:,3));
    minZ = min(verts(:,3));
    
    
    h = figure();
    [numVerts, ~] = size(verts);
    colorValue = repmat([224, 235, 235],numVerts, 1);
    pcshow(verts, colorValue);
    % C crotch len, the vertical distance
    pts = verts(landmarksIdx.C_idx, :);
%     pts(1,1) = pts(2,1); % set the same x and z values
%     pts(1,3) = pts(2,3);
    pts(1,1) = 0;
    pts(2,1) = 0;
    pts(1,3) = (minZ+maxZ)/2;
    pts(2,3) = (minZ+maxZ)/2;
    plotInsectPoints(h, pts, 'yx', 10)
    plotStraightLine(h, pts, 'y-', 2)
    
    % Overall height, the verstical line
    pts = [minX-5, minY, 0; minX-5, maxY, 0];
    plotStraightLine(h, pts, 'y-', 2)
    
    %
    plotInsectPoints(h, verts(landmarksIdx.J_idx_left, :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.J_idx_left, :), 'y-', 2)
    
    plotInsectPoints(h, verts(landmarksIdx.J_idx_right, :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.J_idx_right, :), 'y-', 2)
    
    plotInsectPoints(h, verts(landmarksIdx.K_idx_left, :),  'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.K_idx_left, :),  'y-', 2)
    
    plotInsectPoints(h, verts(landmarksIdx.K_idx_right, :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.K_idx_right, :), 'y-', 2)

    plotStraightLine(h, insectPts.A, 'r-', 2) % A head circ
%     plotInsectPoints(h, verts(landmarksIdx.A_idx,:), 'bx', 10)
    
    plotStraightLine(h, insectPts.B, 'r-', 2) % B neck circ
%     plotInsectPoints(h, verts(landmarksIdx.B_idx,:), 'bx', 10)
    
    plotStraightLine(h, insectPts.D, 'r-', 2) % D chest circ
%     plotInsectPoints(h, verts(landmarksIdx.D_idx,:), 'bx', 10)
    
    plotStraightLine(h, insectPts.E, 'r-', 2) % E waist circ
%     plotInsectPoints(h, verts(landmarksIdx.E_idx,:), 'bx', 10)
    
    plotStraightLine(h, insectPts.F, 'r-', 2) % F pelvis circ
%     plotInsectPoints(h, verts(landmarksIdx.F_idx,:), 'bx', 10)
    
    plotStraightLine(h, insectPts.G_left, 'r-', 2) % G wrist circ, left
%     plotInsectPoints(h, verts(landmarksIdx.G_idx_left,:), 'bx', 10)
    plotStraightLine(h, insectPts.G_right, 'r-', 2) % G wrist circ, right
%     plotInsectPoints(h, verts(landmarksIdx.G_idx_right,:), 'bx', 10)
    
    plotStraightLine(h, insectPts.H_left, 'r-', 2) % H bicep circ left
%     plotInsectPoints(h, verts(landmarksIdx.H_idx_left,:), 'bx', 10)
    plotStraightLine(h, insectPts.H_right, 'r-', 2) % H bicep circ right
%     plotInsectPoints(h, verts(landmarksIdx.H_idx_right,:), 'bx', 10)
    
    plotStraightLine(h, insectPts.I_left, 'r-', 2) % I forearm circ left
%     plotInsectPoints(h, verts(landmarksIdx.I_idx_left,:), 'bx', 10)
    plotStraightLine(h, insectPts.I_right, 'r-', 2) % I forearm circ right
%     plotInsectPoints(h, verts(landmarksIdx.I_idx_right,:), 'bx', 10)
    
    plotStraightLine(h, insectPts.L_left, 'r-', 2) % Thight left
%     plotInsectPoints(h, verts(landmarksIdx.L_idx_left,:), 'bx', 10)
    plotStraightLine(h, insectPts.L_right, 'r-', 2) % Thight right
%     plotInsectPoints(h, verts(landmarksIdx.L_idx_right,:), 'bx', 10)

    plotStraightLine(h, insectPts.M_left, 'r-', 2) % Calf left
%     plotInsectPoints(h, verts(landmarksIdx.M_idx_left,:), 'bx', 10)
    plotStraightLine(h, insectPts.M_right, 'r-', 2) % Calf right
%     plotInsectPoints(h, verts(landmarksIdx.M_idx_right,:), 'bx', 10)
    
    plotStraightLine(h, insectPts.N_left, 'r-', 2) % N ankle left
%     plotInsectPoints(h, verts(landmarksIdx.N_idx_left,:), 'bx', 10)
    plotStraightLine(h, insectPts.N_right, 'r-', 2) % N ankle right
%     plotInsectPoints(h, verts(landmarksIdx.N_idx_right,:), 'bx', 10)
    
    xlim([minX-30, maxX+30]);
    ylim([minY-30, maxY+30]);
end

function plotStraightLine(h, pts, markerColor, lineWidth)
    figure(h)
    hold on
    plot3(pts(:,1), pts(:,2), pts(:,3), ...
          markerColor, 'LineWidth', lineWidth); 
    hold off
end

function plotInsectPoints(h, pts, markerColor, markerSize)
    figure(h)
    hold on
    [nums, ~] = size(pts);
    
    for idx = 1:nums
       plot3(pts(idx, 1), ...
             pts(idx, 2), ...
             pts(idx, 3), ...
             markerColor, 'MarkerSize', markerSize); 
    end
    hold off
end
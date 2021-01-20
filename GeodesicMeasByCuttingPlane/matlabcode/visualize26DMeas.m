function visualize26DMeas(verts, landmarksIdx, insectPts)
    minY = min(verts(:,2));
    maxY = max(verts(:,2));
    minX = min(verts(:,1));
    maxX = max(verts(:,1));
    
    h = figure();
    [numVerts, ~] = size(verts);
    colorValue = repmat([224, 235, 235],numVerts, 1);
    pcshow(verts, colorValue);
    
    % the vertical distance
    plotVerticalLine(h, verts, landmarksIdx.idx16); % head len
    plotVerticalLine(h, verts, landmarksIdx.idx17); % neck len
    plotVerticalLine(h, verts, landmarksIdx.idx19); % upperTorso len
    plotVerticalLine(h, verts, landmarksIdx.idx20); % pelvis len
        
    % the straight distance
    plotInsectPoints(h, verts(landmarksIdx.idx18, :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.idx18, :), 'y-', 2)
    
    plotInsectPoints(h, verts(landmarksIdx.idx21_left,  :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.idx21_left,  :), 'y-', 2)
    plotInsectPoints(h, verts(landmarksIdx.idx21_right, :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.idx21_right, :), 'y-', 2)
    
    plotInsectPoints(h, verts(landmarksIdx.idx22_left,  :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.idx22_left,  :), 'y-', 2)
    plotInsectPoints(h, verts(landmarksIdx.idx22_right, :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.idx22_right, :), 'y-', 2)
    
    plotInsectPoints(h, verts(landmarksIdx.idx23_left,  :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.idx23_left,  :), 'y-', 2)
    plotInsectPoints(h, verts(landmarksIdx.idx23_right, :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.idx23_right, :), 'y-', 2)
    
    plotInsectPoints(h, verts(landmarksIdx.idx24_left,  :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.idx24_left,  :), 'y-', 2)
    plotInsectPoints(h, verts(landmarksIdx.idx24_right, :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.idx24_right, :), 'y-', 2)
    
    plotInsectPoints(h, verts(landmarksIdx.idx25_left,  :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.idx25_left,  :), 'y-', 2)
    plotInsectPoints(h, verts(landmarksIdx.idx25_right, :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.idx25_right, :), 'y-', 2)
    
    plotInsectPoints(h, verts(landmarksIdx.idx26_left,  :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.idx26_left,  :), 'y-', 2)
    plotInsectPoints(h, verts(landmarksIdx.idx26_right, :), 'yx', 10)
    plotStraightLine(h, verts(landmarksIdx.idx26_right, :), 'y-', 2)
    
    % Overall height, the verstical line
    pts = [minX-5, minY, 0; minX-5, maxY, 0];
    plotStraightLine(h, pts, 'y-', 2)
    
    % the Circumference insection points
    plotStraightLine(h, insectPts.insectPt_01, 'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_02, 'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_03, 'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_04, 'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_05, 'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_06, 'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_07, 'r-', 2)
   
    plotStraightLine(h, insectPts.insectPt_08_left,  'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_08_right, 'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_09_left,  'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_09_right, 'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_10_left,  'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_10_right, 'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_11_left,  'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_11_right, 'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_12_left,  'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_12_right, 'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_13_left,  'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_13_right, 'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_14_left,  'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_14_right, 'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_15_left,  'r-', 2) 
    plotStraightLine(h, insectPts.insectPt_15_right, 'r-', 2) 
    
    xlim([minX-30, maxX+30]);
    ylim([minY-30, maxY+30]);
end

function plotVerticalLine(h, verts, landmarksIdx)
    pts = verts(landmarksIdx, :);
    % set the same x and z values
    pts(1,1) = pts(2,1); 
    pts(1,3) = pts(2,3);
    plotInsectPoints(h, pts, 'yx', 10)
    plotStraightLine(h, pts, 'y-', 2)
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
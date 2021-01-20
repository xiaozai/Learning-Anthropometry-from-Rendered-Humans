% to get Intersection points between a plane and mesh
% 
% Song Yan, 2019.09.18
%
% Input: 
%       verts,    the vertices of the mesh
%       tris,     the faces of the mesh
%       normal,   the normal of the cutting plane
%       V0,       any point on the plane
%       plotFlag, true or false
%
% Output:
%       insectPoints, the set of the intersection Points in clockwise order
%
%--------------------------------------------------------------------------
% original implements:  to find the intersect point for each Edge
%
%     for ii = 1:length(edges)
% 
%         P1 = verts(edges(ii, 1), :);
%         P0 = verts(edges(ii, 2), :);
% 
%         u = P1 - P0;
%         w = P0 - V0;
%         D = dot(n, u); % if dot(n,u) ==0, then n is perpendicular to u
%         N = -dot(n, w);
%         I = [0, 0, 0];
%         % if parallel, there are two case: lies inide plane or outside 
%         if abs(D) < 10^-7  % the line segment is parallel to plane
%             if N == 0
%                check = 2;  % the line segment lies in plane
%             else
%                 check = 0; % no intersection
%             end
%         else
%             % if not parallel, there must be one intersection points
%             % the intersection point is :
%             %         P(sI) = P0 + sI .* u
%             % then n is perpendicular to (P(sI) - V0) = P0 - V0 + sI.*u
%             %         dot(n, P(sI) -V0) = 0
%             %      n.*(P0 - V0 + sI.*u) = 0
%             %            n.*(w + sI.*u) = 0 
%             %                        sI = -n.*w / u
%             %
%             % compute the intersection parameter
%             sI = N / D;
%             I = P0 + sI.* u;
%             if (sI < 0 || sI > 1)
%                 check = 3; % the intersection point lies outside the segment
%             else
%                 check = 1; % one intersection points lies in the segment
%             end
%         end
%             
%         if check == 2
%             insectPoints = [insectPoints; P0; P1];
%         elseif check == 1
%             insectPoints = [insectPoints; I];
%         end
%         insectPoints = unique(insectPoints, 'rows');
%     end
%
function [insectPoints] = getInsectPoints(verts, tris, normal, V0, plotFlag)
    % 1) convert the triangles into Edges (e1, e2)
    edges = [tris(:, 1), tris(:,2); tris(:,2), tris(:,3); tris(:, 1), tris(:, 3)];
    edges = sort(edges, 2);
    edges = unique(edges, 'rows');
    
    % 2) fine the intersection points between the edges and the plane
    P1 = verts(edges(:, 1), :);
    P0 = verts(edges(:, 2), :);
    
    u = P1 - P0;
    w = P0 - V0;
    n = repmat(normal, [length(edges),1]);
    
    D = dot(n, u, 2); % if dot(n,u) ==0, then n is perpendicular to u
    N = -dot(n, w, 2);
    
    insectPoints = [];
    % 1) if parallel, there are two case: lies inide plane or outside
    % the line segment lies in plane: dot(n, u) = 0 and dot(n, w) = 0
    % the line segment is parallel to the plane and P0 is in the plane
    parallelEdgeIdx = find((abs(D) < 10^-7) & (N == 0));
    insectPoints = [insectPoints; P0(parallelEdgeIdx, :); P1(parallelEdgeIdx, :)];
    % 2) if not parallel, there must be one intersection point
    % check the intersection points are in the line segment or outside
    % sI should be [0, 1]
    insectIdx = find(abs(D) >= 10^-7); 
    sI = N(insectIdx, :) ./ D(insectIdx, :);
    insideLineIdx = find(sI >=0 & sI <=1); 
    I = P0(insectIdx(insideLineIdx), :) + sI(insideLineIdx).*u(insectIdx(insideLineIdx), :);
    insectPoints = [insectPoints; I];
    insectPoints = unique(insectPoints, 'rows');
    % sort the insectPoints in clock-wise order
    centerInsectPoints = mean(insectPoints);
    P = insectPoints - centerInsectPoints;
    [~, ~, V] = svd(P, 0); % svd can be interpreted as rotation and scaling
    [~,is] = sort(atan2(P*V(:,1),P*V(:,2)));
    if ~isempty(insectPoints)
        insectPoints = insectPoints(is([1:end 1]), :); % add the first point
    end
    
    if plotFlag
        figure()
        h1 = trimesh(tris, verts(:, 1), verts(:,2), verts(:,3));
        hold on
        h2 = scatter3(insectPoints(:,1), insectPoints(:, 2), insectPoints(:,3), 'r');
        plot3(insectPoints(:,1), insectPoints(:, 2), insectPoints(:,3));
        hold off
        xlabel('x'); ylabel('y'); zlabel('z');
        title('body part vertices and faces')
        legend([h1, h2], 'body part mesh', 'intersection points');

        figure()
        scatter3(insectPoints(:,1), insectPoints(:, 2), insectPoints(:,3));
        hold on
        plot3(insectPoints(:,1), insectPoints(:, 2), insectPoints(:,3));
        hold off
        xlabel('x'); ylabel('y'); zlabel('z');
        title('the intersection points')
        
        figure()
        h1 = trimesh(tris, verts(:, 1), verts(:,2), verts(:,3));
        hold on
        w = null(normal);
        [P, Q] = meshgrid(-120:120);
        X = V0(1)+w(1,1)*P+w(1,2)*Q;
        Y = V0(2)+w(2,1)*P+w(2,2)*Q;
        Z = V0(3)+w(3,1)*P+w(3,2)*Q;
        surf(X,Y,Z)
    end
    
end
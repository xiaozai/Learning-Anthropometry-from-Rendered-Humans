% To find the bounder of the vertices

function bound = find_bound(v, f)
    f = double(f);
    v = double(v);
    TR = triangulation(f, v);
    FF = freeBoundary(TR);
    bound = FF(:,1);
end
function vid = readVidText(fname)
    vid = [];
    
    fid = fopen(fname);
    tline = fgetl(fid);
    while ischar(tline)
        C = strsplit(tline);
        if strcmp(C{1}, 'v')
            numIdx = length(C);
            for idx = 2:numIdx
               vid = [vid,  str2double(C{idx})];
            end
        end
        tline = fgetl(fid);
    end
    
    fclose(fid);

end
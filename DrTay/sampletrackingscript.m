cont_nuc = 'control_nucleus.tif';
cont_sensor = 'control_sensor.tif';
treat_nuc = 'treated_nucleus.tif';
treat_sensor = 'treated_sensor.tif';
fr = 24; %minutes per frame
mag = 10; %X
pix_sz = 0.65; %um/px
[control_linker, control_numcells, control_frames] = mv(cont_nuc, cont_sensor);
[treat_linker, treat_numcells, treat_frames] = mv(treat_nuc, treat_sensor);
control_intensities = avg_frame_intens(control_frames, control_linker);
treat_intensities = avg_frame_intens(treat_frames, treat_linker);

%Axis Values
image_len = numel(imfinfo(cont_nuc))*fr;
timeVec = [1:fr:image_len];

figure(1);

%Intensities over Time
subplot(1, 2, 1);
plot(timeVec, control_intensities, 'DisplayName', 'Control')
hold on
plot(timeVec, treat_intensities, 'DisplayName', 'Treated')
hold off
xlabel('Time (mins)')
ylabel('Mean Frame Intensity')
legend

%Number of Cells Over Time
subplot(1, 2, 2);
plot(timeVec, control_numcells, 'DisplayName','Control')
hold on
plot(timeVec, treat_numcells, 'DisplayName', 'Treated')
hold off
xlabel('Time (mins)')
ylabel('Cells (#)')
legend

function [linker, numcells, numFrames1] = mv(Mpath, Ipath)
    fileInfo1 = imfinfo(Mpath);
    numFrames1 = numel(fileInfo1);
    fileInfo2 = imfinfo(Ipath);
    numFrames2 = numel(fileInfo2);
    fprintf('File : %s -- %d Frames\n', Mpath, numFrames1)
    fprintf('File : %s -- %d Frames\n', Ipath, numFrames2) 
    linker = LAPLinker;
    linker.LinkScoreRange = [0, 30];
    numcells = NaN(1,numFrames1);
    for i = 1:numFrames1
        fprintf('Analyzing Frame %d\n', i);
        NI = imread(Mpath, i);
        SI = imread(Ipath, i);
        M1 = imbinarize(NI, 'adaptive');
        M2 = bwareaopen(M1, 25);
        M3 = imclose(M2, strel('disk', 5));
        M4 = imclearborder(M3);
        dd = -bwdist(~M4);
        dd(~M4) = -Inf;
        dd2 = imhmin(dd, 0.7);
        L = watershed(dd2);
        M4(L==0) = false;
%         imshowpair(SI, bwperim(M4))
        data = regionprops(M4, SI, 'Area', 'Centroid', 'MeanIntensity');
        areas = cat(1, data.Area);
        data(areas <= 5) = [];
        data = rmfield(data, 'Area');
        linker = assignToTrack(linker, i, data);
        frame_intens = cat(1, data.MeanIntensity);
        cell_count = numel(frame_intens);
        numcells(i) = cell_count;
        fprintf('Completed\n')
    end
end

function frame_intens = avg_frame_intens(num_frames, linker)
    M = NaN(linker.NumTracks, num_frames);
    for track = [1:linker.NumTracks]
        cur_track = getTrack(linker, track);
        M(track, cur_track.Frames) = cur_track.MeanIntensity;
    end
    frame_intens = mean(M, 1, 'omitnan');
end

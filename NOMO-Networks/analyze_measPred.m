clear; close all; clc;

% gtDir = '/home/yan/Data2/narvi_folder/Pre-Process-CAESARfits/CAESAR-Fits01/male-geodesic-meas/26D-Meas-Labels/';
% predDir = './exp/male_224x224Silh_26D_group10_hks/prediction/';
% outDir = './exp/male_224x224Silh_26D_group10_hks/';

gtDir   = '/home/yan/Data2/narvi_folder/Pre-Process-CAESARfits/CAESAR-Fits01/male-geodesic-meas/16D-Meas-Labels/';
predDir = './exp/male_224x224Silh_16D_group10_alexnet/prediction/';
outDir  = './exp/male_224x224Silh_16D_group10_alexnet/';

sampleList = dir([predDir '*.mat']);
numSamples = length(sampleList);

numMeas = 16;

measNames26D = ...
{'01-headCirc',      '02-neckCirc',    '03-chestCirc',        ...
 '04-underBustCirc', '05-maxWaistCirc','06-trouserWaistCirc', ...
 '07-pelvisCirc',    '08-thighCirc',   '09-kneeCirc',         ...
 '10-calfCirc',      '11-ankleCirc',   '12-bicepCirc',        ...
 '13-elbowCirc',     '14-forearmCirc', '15-wristCirc',        ...
 '16-headLen',       '17-neckLen',     '18-shoulderBreadth',  ... 
 '19-upperTorsoLen', '20-pelvisLen',   '21-upperLegLen' ,     ...
 '22-lowerLegLen' ,  '23-upperRrmLen', '24-lowerArmLen'  ,    ...
 '25-handLen' ,      '26-footLen'};

measNames16D = ...
{'A-HeadCirc',  'B-NeckCirc',     'C-ShouldBladeLen', ...
 'D-ChestCirc', 'E-WaistCirc',    'F-PelvisCirc',     ...
 'G-WristCirc', 'H-BicepCirc',    'I-ForearmCirc',    ...
 'J-armLen',    'K-InsideLegLen', 'L-ThighCirc',      ...
 'M-CalfCirc',  'N-AnkleCirc',    'O-OverallHeight',  ...
 'P-shoulderBreadth'};

if numMeas == 16
    measNames = measNames16D;
else
    measNames = measNames26D;
end

step = 5;

for measIdx = 1:numMeas

    measName = measNames{measIdx};
    
    gtMeas = [];
    predMeas = [];

    for ii = 1:numSamples
        sname = sampleList(ii).name;
        load([gtDir sname]);
        load([predDir sname]);

        gtMeas = [gtMeas, y(measIdx)];
        predMeas = [predMeas, pred(measIdx)];
    end

    % sort the gt
    [gtMeas, gtIdx] = sort(gtMeas);
    predMeas = predMeas(gtIdx);

    fig = figure();
    h2 = plot(1:step:numSamples, predMeas(1:step:numSamples), 'rx');
    hold on 
    h1 = plot(1:step:numSamples, gtMeas(1:step:numSamples), 'gx');
    for ii = 1:step:numSamples
         plot([ii, ii], [predMeas(ii), gtMeas(ii)], 'b-');
    end
    hold off
    title(measName);
    legend([h1, h2], 'ground truth', 'prediction');
    saveas(fig, [outDir measName, '.png']);
end
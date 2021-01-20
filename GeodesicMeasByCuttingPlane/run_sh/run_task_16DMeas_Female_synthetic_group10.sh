#!/bin/bash

#SBATCH -J 16DFSX
#SBATCH --output=/home/yans/GeodesicMeasByCuttingPlane/logs/16D-female-synth-group10-log-output.txt
#SBATCH --error=/home/yans/GeodesicMeasByCuttingPlane/logs/16D-female-synth-group10-log-error.txt
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=2
#SBATCH --time=4-00:00:00
#SBATCH --mem=14000
#SBATCH --partition=normal

module load matlab

matlab -nodisplay -nosplash -nodesktop -r "run('/home/yans/GeodesicMeasByCuttingPlane/matlabcode/get16DMeas_CAESAR_synthetic_female_group10.m');exit"

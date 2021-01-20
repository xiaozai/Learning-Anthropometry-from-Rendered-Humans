#!/bin/bash

#SBATCH -J 27D10
#SBATCH --output=../logs/27D-male-synth10-log-output.txt
#SBATCH --error=../logs/27D-male-synth10-log-error.txt
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=2
#SBATCH --time=4-00:00:00
#SBATCH --mem=14000
#SBATCH --partition=normal

module load matlab

matlab -nodisplay -nosplash -nodesktop -r "run('../matlabcode/getExtraMeas_CAESAR_synthetic_group10.m');exit"

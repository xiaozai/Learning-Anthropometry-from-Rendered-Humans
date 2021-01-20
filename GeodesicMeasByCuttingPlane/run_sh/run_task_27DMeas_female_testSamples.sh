#!/bin/bash

#SBATCH -J 27DT2
#SBATCH --output=../logs/27D-female-synth-test-log-output.txt
#SBATCH --error=../logs/27D-female-synth-test-log-error.txt
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=2
#SBATCH --time=4-00:00:00
#SBATCH --mem=14000
#SBATCH --partition=normal

module load matlab

matlab -nodisplay -nosplash -nodesktop -r "run('../matlabcode/getExtraMeas_female_testsamples.m');exit"

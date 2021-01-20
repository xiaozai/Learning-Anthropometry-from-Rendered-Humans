#!/bin/bash

#SBATCH -J 26DMSX
#SBATCH --output=logs/26D-male-synth-group10-log-output.txt
#SBATCH --error=logs/26D-male-synth-group10-log-error.txt
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=2
#SBATCH --time=4-00:00:00
#SBATCH --mem=14000
#SBATCH --partition=normal

module load matlab

matlab -nodisplay -nosplash -nodesktop -r "run('get26DMeas_CAESAR_synthetic_male_group10.m');exit"

#!/bin/bash

#SBATCH -J 26DF
#SBATCH --output=logs/26D-female-log-output.txt
#SBATCH --error=logs/26D-female-log-error.txt
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=2
#SBATCH --time=4-00:00:00
#SBATCH --mem=14000
#SBATCH --partition=normal

module load matlab

matlab -nodisplay -nosplash -nodesktop -r "run('get26DMeas_CAESAR_Fits01_female.m');exit"

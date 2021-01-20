#!/bin/bash

#SBATCH -J 16DFN
#SBATCH --output=logs/16D-female-nicp-log-output.txt
#SBATCH --error=logs/16D-female-nicp-log-error.txt
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=2
#SBATCH --time=4-00:00:00
#SBATCH --mem=14000
#SBATCH --partition=normal

module load matlab

matlab -nodisplay -nosplash -nodesktop -r "run('get16DMeas_CAESAR_Fits01_female.m');exit"

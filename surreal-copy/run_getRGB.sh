#!/bin/bash

#SBATCH -J su01_0
#SBATCH --output=/home/yans/surreal-master/datageneration/logs/CAESARfits01-male-group01_00-log-output.txt
#SBATCH --error=/home/yans/surreal-master/datageneration/logs/CAESARfits01-male-group01_00-log-error.txt
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=2
#SBATCH --time=7-00:00:00
#SBATCH --mem=64000
#SBATCH --partition=normal

source activate python2_env

# SET PATHS HERE
FFMPEG_PATH=/home/yans/surreal-master/tools/ffmpeg-4.1.4/ffmpeg_build_sequoia_h264
X264_PATH=/home/yans/surreal-master/tools/ffmpeg-4.1.4/x264_build/
BLENDER_PATH=/home/yans/surreal-master/blender-2.78a
# BUNLED PYTHON
BUNDLED_PYTHON=${BLENDER_PATH}/2.78/python
export PYTHONPATH=${BUNDLED_PYTHON}/lib/python3.5:${BUNDLED_PYTHON}/lib/python3.5/site-packages
export PYTHONPATH=${BUNDLED_PYTHON}:${PYTHONPATH}
# FFMPEG
export LD_LIBRARY_PATH=${FFMPEG_PATH}/lib:${X264_PATH}/lib:${LD_LIBRARY_PATH}
export PATH=${FFMPEG_PATH}/bin:${PATH}

### RUN PART 1  --- Uses python3 because of Blender
JOB_PARAMS=${1:-'--startIdx 10 --endIdx 1000 --gender male --Sample_Dir /home/yans/Pre-Process-CAESARfits/CAESAR-Fits01/male-synthetic-samples/20D-PCA/obj_withVT_meter/group01/ --tmp_path /home/yans/surreal-master/datageneration/datasets/SURREAL/CAESAR-Fits01-01_01/ --output_path /home/yans/Pre-Process-CAESARfits/CAESAR-Fits01/male-synthetic-samples/20D-PCA/img/group01/'}

$BLENDER_PATH/blender -b -t 1 -P /home/yans/surreal-master/datageneration/main_part1_loadObj.py -- ${JOB_PARAMS}


conda deactivate

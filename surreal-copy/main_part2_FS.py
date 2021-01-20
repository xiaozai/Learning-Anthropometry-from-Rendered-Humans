import os 
from os.path import join, exists
import numpy as np
import scipy.io
import config
import time

import OpenEXR   # to read exr imgs
import array
import Imath

start_time = None
def log_message(message):
    elapsed_time = time.time() - start_time
    print("[%.2f s] %s" % (elapsed_time, message))

def mkdir_safe(directory):
    try:
        os.makedirs(directory)
    except FileExistsError:
        pass
#----------------------------------------------------------
if __name__ == '__main__':

    start_time = time.time()
    log_message("start part 2")

    gender     = 'male'
    
    # params      = config.load_file('config', 'SYNTH_DATA')
    # resy        = params['resy']
    # resx        = params['resx']
    # tmp_path    = params['tmp_path']
    # output_path = params['output_path']

    params = {}
    params['resy'] = 640
    params['resx'] = 640
    params['tmp_path'] = '/home/yan/Data2/Projects/surreal-master/datageneration/datasets/SURREAL/tmp/'
    params['output_path'] = '/home/yan/Data2/Projects/surreal-master/datageneration/datasets/SURREAL/'

    resy        = params['resy']
    resx        = params['resx']
    tmp_path    = params['tmp_path']
    output_path = params['output_path']


    get_real_frame = lambda ifr: ifr

    FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)

    output_depth_path = join(output_path, gender, 'depth')
    output_segm_path  = join(output_path, gender, 'segm')

    if not exists(output_depth_path):
        mkdir_safe(output_depth_path)
    if not exists(output_segm_path):
        mkdir_safe(output_segm_path)

    #------------------------------------------------------------
    sampleList = os.listdir('/home/yan/Data2/Projects/NOMO-Dataset/NOMO-fits/NICP_iter02/%s/'%gender)

    N_MESH = len(sampleList)
    for ishape in range(N_MESH):
        
        name = sampleList[ishape][:-4]

        tmp_depth_path = join(tmp_path, '%s_depth'%name)  # mesh01_depth/
        tmp_segm_path  = join(tmp_path, '%s_segm'%name)   # mesh01_segm/
        matfile_depth  = join(output_depth_path, name + "_depth.mat") # mesh01_depth.mat
        matfile_segm   = join(output_segm_path, name + "_segm.mat")   # mesh01_segm.mat
        dict_depth     = {}
        dict_segm      = {}
        #------------------------------------------------------------------------------
        # Convert EXR file to mat, 0 for front-view, 1 for side-view
        for seg_frame in range(1, 3):
            # depth 
            path = join(tmp_depth_path, 'Image%04d.exr' % get_real_frame(seg_frame))
            exr_file = OpenEXR.InputFile(path)
            mat = np.reshape([array.array('f', exr_file.channel(Chan, FLOAT)).tolist() for Chan in ("R")], (resx, resy))
            dict_depth['depth_%d'%seg_frame] = mat.astype(np.float32, copy=False)
            # segm
            path = join(tmp_segm_path, 'Image%04d.exr' % get_real_frame(seg_frame))
            exr_file = OpenEXR.InputFile(path)
            mat = np.reshape([array.array('f', exr_file.channel(Chan, FLOAT)).tolist() for Chan in ("R")], (resx, resy))
            dict_segm['segm_%d' %seg_frame] = mat.astype(np.uint8, copy=False)

        scipy.io.savemat(matfile_depth, dict_depth, do_compression=True)
        scipy.io.savemat(matfile_segm,  dict_segm, do_compression=True)

    # cleaning up tmp
    if tmp_path != "" and tmp_path != "/":
        log_message("Cleaning up tmp")
        os.system('rm -rf %s' % tmp_path)

    log_message("Completed batch")
import sys
import os
import random
import math
import bpy
import numpy as np
from os import getenv
from os import remove
from os.path import join, dirname, realpath, exists
from mathutils import Matrix, Vector, Quaternion, Euler
from glob import glob
from random import choice
from pickle import load
import scipy.io
from bpy_extras.object_utils import world_to_camera_view as world2cam

import argparse
parser = argparse.ArgumentParser(description='Generate synth dataset images.')
parser.add_argument('--startIdx',    type=int, default=0)
parser.add_argument('--endIdx',      type=int, default=0)
parser.add_argument('--gender',      default='male')
parser.add_argument('--clothing_option', default='grey')
parser.add_argument('--Sample_Dir',  default='/home/yans/Pre-Process-CAESARfits/CAESAR-Fits02/male-withVT/')
parser.add_argument('--tmp_path',    default='/home/yans/surreal-master/datageneration/datasets/SURREAL/CAESAR-Fits02/')
parser.add_argument('--output_path', default='/home/yans/Pre-Process-CAESARfits/CAESAR-Fits02/male-rendered-imgs/')


sys.path.insert(0, ".")

def mkdir_safe(directory):
    try:
        os.makedirs(directory)
    except FileExistsError:
        pass

def setState0():
    for ob in bpy.data.objects.values():
        ob.select=False
    bpy.context.scene.objects.active = None

sorted_parts = ['hips','leftUpLeg','rightUpLeg','spine','leftLeg','rightLeg',
                'spine1','leftFoot','rightFoot','spine2','leftToeBase','rightToeBase',
                'neck','leftShoulder','rightShoulder','head','leftArm','rightArm',
                'leftForeArm','rightForeArm','leftHand','rightHand','leftHandIndex1' ,'rightHandIndex1']
# order
part_match = {'root':'root', 'bone_00':'Pelvis', 'bone_01':'L_Hip', 'bone_02':'R_Hip',
              'bone_03':'Spine1', 'bone_04':'L_Knee', 'bone_05':'R_Knee', 'bone_06':'Spine2',
              'bone_07':'L_Ankle', 'bone_08':'R_Ankle', 'bone_09':'Spine3', 'bone_10':'L_Foot',
              'bone_11':'R_Foot', 'bone_12':'Neck', 'bone_13':'L_Collar', 'bone_14':'R_Collar',
              'bone_15':'Head', 'bone_16':'L_Shoulder', 'bone_17':'R_Shoulder', 'bone_18':'L_Elbow',
              'bone_19':'R_Elbow', 'bone_20':'L_Wrist', 'bone_21':'R_Wrist', 'bone_22':'L_Hand', 'bone_23':'R_Hand'}

part2num = {part:(ipart+1) for ipart,part in enumerate(sorted_parts)}

# create one material per part as defined in a pickle with the segmentation
# this is useful to render the segmentation in a material pass
def create_segmentation(ob, params):
    materials = {}
    vgroups = {}
    with open('/home/yans/surreal-master/datageneration/pkl/segm_per_v_overlap.pkl', 'rb') as f:
        vsegm = load(f)
    bpy.ops.object.material_slot_remove()
    parts = sorted(vsegm.keys())
    for part in parts:
        vs = vsegm[part]
        vgroups[part] = ob.vertex_groups.new(part)
        vgroups[part].add(vs, 1.0, 'ADD')
        bpy.ops.object.vertex_group_set_active(group=part)
        materials[part] = bpy.data.materials['Material'].copy()
        materials[part].pass_index = part2num[part]
        bpy.ops.object.material_slot_add()
        ob.material_slots[-1].material = materials[part]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.material_slot_assign()
        bpy.ops.object.mode_set(mode='OBJECT')
    return(materials)

# create the different passes that we render
def create_composite_nodes(tree, params, img=None, name=None):
    res_paths = {k:join(params['tmp_path'], '%s_%s'%(name, k)) for k in params['output_types'] if params['output_types'][k]}
    
    # clear default nodes
    for n in tree.nodes:
        tree.nodes.remove(n)

    # create node for foreground image
    layers = tree.nodes.new('CompositorNodeRLayers')
    layers.location = -300, 400

    # create node for background image
    bg_im = tree.nodes.new('CompositorNodeImage')
    bg_im.location = -300, 30
    if img is not None:
        bg_im.image = img

    # create node for mixing foreground and background images 
    mix = tree.nodes.new('CompositorNodeMixRGB')
    mix.location = 40, 30
    mix.use_alpha = True

    # create node for the final output 
    composite_out = tree.nodes.new('CompositorNodeComposite')
    composite_out.location = 240, 30

    # create node for saving depth
    if(params['output_types']['depth']):
        depth_out = tree.nodes.new('CompositorNodeOutputFile')
        depth_out.location = 40, 700
        depth_out.format.file_format = 'OPEN_EXR'
        depth_out.base_path = res_paths['depth']

    # create node for saving segmentation
    if(params['output_types']['segm']):
        segm_out = tree.nodes.new('CompositorNodeOutputFile')
        segm_out.location = 40, 400
        segm_out.format.file_format = 'OPEN_EXR'
        segm_out.base_path = res_paths['segm']
    
    # merge fg and bg images
    tree.links.new(bg_im.outputs[0], mix.inputs[1])
    tree.links.new(layers.outputs['Image'], mix.inputs[2])
    tree.links.new(mix.outputs[0], composite_out.inputs[0])            # bg+fg image
    
    if(params['output_types']['depth']):    
        tree.links.new(layers.outputs['Z'], depth_out.inputs[0])       # save depth
    if(params['output_types']['segm']):
        tree.links.new(layers.outputs['IndexMA'], segm_out.inputs[0])  # save segmentation

    return(res_paths)

# creation of the spherical harmonics material, using an OSL script
def create_sh_material(tree, sh_path, img=None):
    # clear default nodes
    for n in tree.nodes:
        tree.nodes.remove(n)

    uv = tree.nodes.new('ShaderNodeTexCoord')
    uv.location = -800, 400

    uv_xform = tree.nodes.new('ShaderNodeVectorMath')
    uv_xform.location = -600, 400
    uv_xform.inputs[1].default_value = (0, 0, 1)
    uv_xform.operation = 'AVERAGE'

    uv_im = tree.nodes.new('ShaderNodeTexImage')
    uv_im.location = -400, 400
    if img is not None:
        uv_im.image = img

    rgb = tree.nodes.new('ShaderNodeRGB')
    rgb.location = -400, 200

    script = tree.nodes.new('ShaderNodeScript')
    script.location = -230, 400
    script.mode = 'EXTERNAL'
    script.filepath = sh_path #'spher_harm/sh.osl' #using the same file from multiple jobs causes white texture
    script.update()

    # the emission node makes it independent of the scene lighting
    emission = tree.nodes.new('ShaderNodeEmission')
    emission.location = -60, 400

    mat_out = tree.nodes.new('ShaderNodeOutputMaterial')
    mat_out.location = 110, 400
    
    tree.links.new(uv.outputs[2], uv_im.inputs[0])
    tree.links.new(uv_im.outputs[0], script.inputs[0])
    tree.links.new(script.outputs[0], emission.inputs[0])
    tree.links.new(emission.outputs[0], mat_out.inputs[0])

def init_scene(scene, params, obname='male_0000', gender='female', Flag=True):
    # load obj 
    bpy.ops.import_scene.obj(filepath=join(params['Sample_Dir'], '%s.obj'%obname), axis_forward='Y', axis_up='Z')

    ob = bpy.data.objects[obname]
    ob.data.use_auto_smooth = False  # autosmooth creates artifacts
    
    # assign the existing spherical harmonics material
    ob.active_material = bpy.data.materials['Material']

    # delete the default cube (which held the material)
    if bpy.data.objects.get('Cube') is not None:
        log_message("Delete the Cube")
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['Cube'].select = True
        bpy.ops.object.delete(use_global=False)

    # Add a Lamp
    if bpy.data.objects.get('Lamp') is None:
        log_message("Add a Lamp")
        lamp_data = bpy.data.lamps.new(name="Lamp", type='POINT')          # Create new lamp datablock
        lamp_object = bpy.data.objects.new("Lamp", object_data=lamp_data)  # Create new object with lamp datablock
        scene.objects.link(lamp_object)                                    # Link lamp object to the scene so it will appear
        lamp_object.location=(4.0762, 1.0055, 5.9039)                      # Place lamp to a specified location

    # set camera properties and initial position
    if bpy.data.objects.get('Camera') is None:
        log_message("Add a Camera")
        bpy.ops.object.camera_add()         # Add a camera object to the scene
        scene.camera = bpy.context.object   # Set the scene.camera after adding the camera

    bpy.ops.object.select_all(action='DESELECT')
    cam_ob = bpy.data.objects['Camera']
    scn = bpy.context.scene
    scn.objects.active = cam_ob
    # rotate around Y-axis in 90 degree
    cam_ob.matrix_world = Matrix((( 0.,  0.,  1., params['camera_location'][0]),  # Camera Orientation and Location
                                  ( 0.,  1.,  0., params['camera_location'][1]),  # Camera Loc = [6, 1, 0]
                                  (-1.,  0.,  0., params['camera_location'][2]),
                                  ( 0.,  0.,  0., 1.)))
    cam_ob.data.angle         = math.radians(60)        # Camera lens field of view, FOV
    cam_ob.data.lens          = 60                      # Perspective Camera lens value in millimeters
    cam_ob.data.clip_start    = 0.1                     # Camera near clipping distance
    cam_ob.data.sensor_width  = 32                      # Horizontal size of the image sensor area in millimeters

    # setup an empty object in the center which will be the parent of the Camera
    # this allows to easily rotate an object around the origin
    scn.cycles.film_transparent = True
    scn.render.layers["RenderLayer"].use_pass_vector  = True
    scn.render.layers["RenderLayer"].use_pass_normal  = True
    scene.render.layers['RenderLayer'].use_pass_emit  = True
    scene.render.layers['RenderLayer'].use_pass_emit  = True
    scene.render.layers['RenderLayer'].use_pass_uv    = True
    scene.render.layers['RenderLayer'].use_pass_material_index  = True

    # set render size
    scn.render.resolution_x = params['resy']
    scn.render.resolution_y = params['resx']
    scn.render.resolution_percentage = 100
    scn.render.image_settings.file_format = 'PNG'

    return(ob, obname, cam_ob)

import time
start_time = None
def log_message(message):
    elapsed_time = time.time() - start_time
    print("[%.2f s] %s" % (elapsed_time, message))

#-----------------------------------------------------------------------------------------------
def main():
    # time logging
    global start_time
    start_time = time.time()
    #-------------------------------------------------------------------------------------------
    log_message(sys.argv)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    #-------------------------------------------------------------------------------------------
    # genders = {0: 'female', 1: 'male'}
    # gender  = 'male'
    gender = args.gender 
    #--------------------------------------------------------------------------------------------
    # import configuration
    log_message("Importing configuration")

    params = {}
    params['resy']               = 640
    params['resx']               = 640
    params['camera_location']    = [6, 1, 0]
    params['use_split']          = 'all'
    params['smpl_data_folder']   = '/home/yans/surreal-master/datageneration/smpl_data'
    params['smpl_data_filename'] = 'smpl_data.npz'
    params['bg_path']            = '/home/yans/surreal-master/datageneration/datasets/BG_IMG/'
    params['clothing_option']    = args.clothing_option
    params['tmp_path']           = args.tmp_path
    params['output_path']        = args.output_path
    params['Sample_Dir']         = args.Sample_Dir
    params['output_types']       = {'depth':True, 'fg':False, 'gtflow':False, 'normal':False, 'segm':True, 'vblur':False}
    

    smpl_data_folder   = params['smpl_data_folder']
    smpl_data_filename = params['smpl_data_filename']
    bg_path            = params['bg_path']             # background images path
    resy               = params['resy']                # img width
    resx               = params['resx']                # img height
    clothing_option    = params['clothing_option']     # grey, nongrey or all
    tmp_path           = params['tmp_path']            # save temporary files, EXR files for depth and segm
    output_path        = params['output_path']         # save images
    output_types       = params['output_types']        # segmentation, depth

    # for each clipsize'th frame in the sequence
    get_real_frame = lambda ifr: ifr

    # check if already computed
    #  + clean up existing tmp folders if any
    if exists(tmp_path) and tmp_path != "" and tmp_path != "/":
        os.system('rm -rf %s' % tmp_path)
    
    # create tmp directory
    if not exists(tmp_path):
        mkdir_safe(tmp_path)

    # create output directory
    if not exists(output_path):
        mkdir_safe(output_path)

    rgb_path = join(output_path, 'RGB')

    if not exists(rgb_path):
        mkdir_safe(rgb_path)

    silh_path = join(output_path, 'silh')

    if not exists(silh_path):
        mkdir_safe(silh_path)

    mat_dirname = 'render_info_mat'
    mat_path    = join(output_path, mat_dirname)     # Output Dict Info data path

    if not exists(mat_path):
        mkdir_safe(mat_path)
    #--------------------------------------------------------------------------------------------
    #
    log_message("Setup Blender")
    # create copy-spher.harm. directory if not exists
    sh_dir = join(tmp_path, 'spher_harm')
    if not exists(sh_dir):
        mkdir_safe(sh_dir)

    sh_dst = join(sh_dir, 'sh.osl')
    if not os.path.isfile(sh_dst):
        os.system('cp /home/yans/surreal-master/datageneration/spher_harm/sh.osl %s' % sh_dst)
    # ----------------------------------------------------------------
    log_message("Listing background images")           # Bacground Images Part
    # bg_names = join(bg_path, '%s_img.txt' % params['use_split'])
    bg_names = join(bg_path, 'train_img.txt')
    nh_txt_paths = []
    with open(bg_names) as f:
        for line in f:
            nh_txt_paths.append(join(bg_path, 'img', line))  # Using Clear BG Image
    # grab clothing names
    log_message("clothing: %s" % clothing_option)      # Clothing Image Part
    with open( join(smpl_data_folder, 'textures', '%s_%s.txt' % (gender, params['use_split']) ) ) as f:
        txt_paths = f.read().splitlines()
    # if using only one source of clothing
    if clothing_option == 'nongrey':
        txt_paths = [k for k in txt_paths if 'nongrey' in k]
    elif clothing_option == 'grey':
        txt_paths = [k for k in txt_paths if 'nongrey' not in k]
    #--------------------------------------------------------------------------------------------
    #
    sampleList = os.listdir(params['Sample_Dir'])

    N_MESH = len(sampleList)

    for ishape in range(args.startIdx, args.endIdx):

        name = sampleList[ishape][:-4]
        print("\n\nThe %d-th shape, sName: %s --- \n\n"%(ishape, name))
        
        # Load default file
        bpy.ops.wm.read_factory_settings()

        # delete all objects in the old scene/script
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        #----------------------------------------------------------------
        scene = bpy.data.scenes['Scene']
        scene.render.engine = 'CYCLES'
        bpy.data.materials['Material'].use_nodes = True
        scene.cycles.shading_system = True
        scene.use_nodes = True
        #----------------------------------------
        # random clothing image
        cloth_img_name = choice(txt_paths)
        cloth_img_name = join(smpl_data_folder, cloth_img_name)
        cloth_img = bpy.data.images.load(cloth_img_name)
        # random background
        bg_img_name = choice(nh_txt_paths)[:-1]
        bg_img = bpy.data.images.load(bg_img_name)
        # --------------------------------------------------------------------
        log_message("Building materials tree")
        mat_tree = bpy.data.materials['Material'].node_tree
        create_sh_material(mat_tree, sh_dst, cloth_img)
        res_paths = create_composite_nodes(scene.node_tree, params, img=bg_img, name=name)
        #
        log_message("Initializing scene")
        ob, obname, cam_ob = init_scene(scene, params, obname=name, gender=gender)
        #
        setState0()
        ob.select = True
        bpy.context.scene.objects.active = ob
        # create material segmentation
        log_message("Creating materials segmentation")
        segmented_materials = True #True: 0-24, False: expected to have 0-1 bg/fg
        if segmented_materials:
            materials = create_segmentation(ob, params)
            prob_dressed = {'leftLeg':.5,          'leftArm':.9,      'leftHandIndex1':.01,
                            'rightShoulder':.8,    'rightHand':.01,   'neck':.01,
                            'rightToeBase':.9,     'leftShoulder':.8, 'leftToeBase':.9,
                            'rightForeArm':.5,     'leftHand':.01,    'spine':.9,
                            'leftFoot':.9,         'leftUpLeg':.9,    'rightUpLeg':.9,
                            'rightFoot':.9,        'head':.01,        'leftForeArm':.5,
                            'rightArm':.5,         'spine1':.9,       'hips':.9,
                            'rightHandIndex1':.01, 'spine2':.9,       'rightLeg':.5}
        else:
            materials    = {'FullBody': bpy.data.materials['Material']}
            prob_dressed = {'FullBody': .6}
        #----------------------------------------------------------------------
        # spherical harmonics material needs a script to be loaded and compiled
        scs = []
        for mname, material in materials.items():
            scs.append(material.node_tree.nodes['Script'])
            scs[-1].filepath = sh_dst
            scs[-1].update()

        cam_ob.animation_data_clear()
        #--------------------------------------------------------------------
        # Start to Render
        #
        scene.node_tree.nodes['Image'].image = bg_img
        #
        for part, material in materials.items():
            material.node_tree.nodes['Vector Math'].inputs[1].default_value[:2] = (0, 0)
        # random light
        sh_coeffs    = .7 * (2 * np.random.rand(9) - 1)
        sh_coeffs[0] = .5 + .9 * np.random.rand() # Ambient light (first coeff) needs a minimum  is ambient. 
        sh_coeffs[1] = -.7 * np.random.rand()     # Rest is uniformly distributed, higher means brighter.
        #
        for ish, coeff in enumerate(sh_coeffs):
            for sc in scs:
                sc.inputs[ish+1].default_value = coeff
        #------------------------------------------------------------------
        # Front View Frame
        seq_frame = 1
        scene.frame_set(get_real_frame(seq_frame))
        # ob.rotation_euler = (0, 0.5*np.pi, 0)
        ob.rotation_euler = (0, 0.25*np.pi, 0)
        scene.update()
        # Render
        scene.render.use_antialiasing = False
        # scene.render.filepath = join(rgb_path, 'front', '%s.png' % (name))
        scene.render.filepath = join(rgb_path, '45_degree', '%s.png' % (name))
        #
        for ish, coeff in enumerate(sh_coeffs):
            for sc in scs:
                sc.inputs[ish+1].default_value = coeff
        #
        log_message("Rendering frame %d of %s" % (seq_frame, name))
        # disable render output
        logfile = '/dev/null'
        open(logfile, 'a').close()
        old = os.dup(1)
        sys.stdout.flush()
        os.close(1)
        os.open(logfile, os.O_WRONLY)
        # Render
        bpy.ops.render.render(write_still=True)
        # disable output redirection
        os.close(1)
        os.dup(old)
        os.close(old)
        #---------------------------------------------------------------------------------------------
        # Side View Frame
        seq_frame = 2
        scene.frame_set(get_real_frame(seq_frame))
        # ob.rotation_euler = (0, 0*np.pi, 0)
        ob.rotation_euler = (0, np.pi/3.0, 0)
        scene.update()
        # Render
        scene.frame_set(get_real_frame(seq_frame))
        iframe = seq_frame
        scene.render.use_antialiasing = False
        # scene.render.filepath = join(rgb_path, 'side', '%s.png' % (name))
        scene.render.filepath = join(rgb_path, '30_degree', '%s.png' % (name))
        #
        for ish, coeff in enumerate(sh_coeffs):
            for sc in scs:
                sc.inputs[ish+1].default_value = coeff
        #
        log_message("Rendering frame %d of %s" % (seq_frame, name))
        # disable render output
        logfile = '/dev/null'
        open(logfile, 'a').close()
        old = os.dup(1)
        sys.stdout.flush()
        os.close(1)
        os.open(logfile, os.O_WRONLY)
        # Render
        bpy.ops.render.render(write_still=True)
        # disable output redirection
        os.close(1)
        os.dup(old)
        os.close(old)

        seq_frame = 3
        scene.frame_set(get_real_frame(seq_frame))
        # ob.rotation_euler = (0, 0*np.pi, 0)
        ob.rotation_euler = (0, np.pi/6.0, 0)
        scene.update()
        # Render
        scene.frame_set(get_real_frame(seq_frame))
        iframe = seq_frame
        scene.render.use_antialiasing = False
        # scene.render.filepath = join(rgb_path, 'side', '%s.png' % (name))
        scene.render.filepath = join(rgb_path, '60_degree', '%s.png' % (name))
        #
        for ish, coeff in enumerate(sh_coeffs):
            for sc in scs:
                sc.inputs[ish+1].default_value = coeff
        #
        log_message("Rendering frame %d of %s" % (seq_frame, name))
        # disable render output
        logfile = '/dev/null'
        open(logfile, 'a').close()
        old = os.dup(1)
        sys.stdout.flush()
        os.close(1)
        os.open(logfile, os.O_WRONLY)
        # Render
        bpy.ops.render.render(write_still=True)
        # disable output redirection
        os.close(1)
        os.dup(old)
        os.close(old)

        seq_frame = 4
        scene.frame_set(get_real_frame(seq_frame))
        # ob.rotation_euler = (0, 0*np.pi, 0)
        ob.rotation_euler = (0, np.pi/12.0, 0)
        scene.update()
        # Render
        scene.frame_set(get_real_frame(seq_frame))
        iframe = seq_frame
        scene.render.use_antialiasing = False
        # scene.render.filepath = join(rgb_path, 'side', '%s.png' % (name))
        scene.render.filepath = join(rgb_path, '75_degree', '%s.png' % (name))
        #
        for ish, coeff in enumerate(sh_coeffs):
            for sc in scs:
                sc.inputs[ish+1].default_value = coeff
        #
        log_message("Rendering frame %d of %s" % (seq_frame, name))
        # disable render output
        logfile = '/dev/null'
        open(logfile, 'a').close()
        old = os.dup(1)
        sys.stdout.flush()
        os.close(1)
        os.open(logfile, os.O_WRONLY)
        # Render
        bpy.ops.render.render(write_still=True)
        # disable output redirection
        os.close(1)
        os.dup(old)
        os.close(old)
        #---------------------------------------------------------------------------------------------
        # save annotation excluding png/exr data to _info.mat file
        dict_info = {}
        dict_info['name']   = name
        dict_info['bg']     = bg_img_name
        dict_info['cloth']  = cloth_img_name
        dict_info['gender'] = gender
        dict_info['light']  = sh_coeffs

        matfile_info = join(mat_path, name+'.mat')
        scipy.io.savemat(matfile_info, dict_info, do_compression=True)
#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

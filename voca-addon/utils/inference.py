'''
Max-Planck-Gesellschaft zur Foerderung der Wissenschaften e.V. (MPG) is holder of all proprietary rights on this
computer program.

You can only use this computer program if you have closed a license agreement with MPG or you get the right to use
the computer program from someone who is authorized to grant you that right.

Any use of the computer program without a valid license is prohibited and liable to prosecution.

Copyright 2019 Max-Planck-Gesellschaft zur Foerderung der Wissenschaften e.V. (MPG). acting on behalf of its
Max Planck Institute for Intelligent Systems and the Max Planck Institute for Biological Cybernetics.
All rights reserved.

More information about VOCA is available at http://voca.is.tue.mpg.de.
For comments or questions, please email us at voca@tue.mpg.de
'''

import os
import sys
from pathlib import Path

# get home directory to build the absolute path to virtual environment's python3.7 
homeuserdir = str(Path.home())
abs_path = homeuserdir + '/.virtualenvs/vocablender/lib/python3.7/site-packages'
# get the index of the blender's python lib in $PATH variable
sys_path_index = next(i for i, string in enumerate(sys.path) if 'site-packages' in string)
# insert the virtual environment's python into the sys.path if needed
if not any('.virtualenvs/vocablender' in string for string in sys.path) :
    sys.path.insert(sys_path_index, abs_path)
# print(sys.path)

import tempfile
import numpy as np
import tensorflow as tf
from scipy.io import wavfile
from psbody.mesh import Mesh
from . audio_handler import AudioHandler

def process_audio(ds_path, audio, sample_rate):
    config = {}
    config['deepspeech_graph_fname'] = ds_path
    config['audio_feature_type'] = 'deepspeech'
    config['num_audio_features'] = 29

    config['audio_window_size'] = 16
    config['audio_window_stride'] = 1

    tmp_audio = {'subj': {'seq': {'audio': audio, 'sample_rate': sample_rate}}}
    audio_handler = AudioHandler(config)
    return audio_handler.process(tmp_audio)['subj']['seq']['audio']


def output_sequence_meshes(sequence_vertices, template, out_path, uv_template_fname='', texture_img_fname=''):
    mesh_out_path = os.path.join(out_path, 'meshes')
    if not os.path.exists(mesh_out_path):
        os.makedirs(mesh_out_path)

    if os.path.exists(uv_template_fname):
        uv_template = Mesh(filename=uv_template_fname)
        vt, ft = uv_template.vt, uv_template.ft
    else:
        vt, ft = None, None

    num_frames = sequence_vertices.shape[0]
    for i_frame in range(num_frames):
        out_fname = os.path.join(mesh_out_path, '%05d.obj' % i_frame)
        out_mesh = Mesh(sequence_vertices[i_frame], template.f)
        if vt is not None and ft is not None:
            out_mesh.vt, out_mesh.ft = vt, ft
        if os.path.exists(texture_img_fname):
            out_mesh.set_texture_image(texture_img_fname)
        out_mesh.write_obj(out_fname)


def inference(tf_model_fname, ds_fname, audio_fname, template_fname, condition_idx, out_path):
    template = Mesh(filename=template_fname)

    sample_rate, audio = wavfile.read(audio_fname)
    if audio.ndim != 1:
        print('Audio has multiple channels, only first channel is considered')
        audio = audio[:,0]

    processed_audio = process_audio(ds_fname, audio, sample_rate)

    # Load previously saved meta graph in the default graph
    #saver = tf.train.import_meta_graph(tf_model_fname + '.meta')
    saver = tf.compat.v1.train.import_meta_graph(tf_model_fname + '.meta')
    #graph = tf.get_default_graph()
    graph = tf.compat.v1.get_default_graph()
    
    speech_features = graph.get_tensor_by_name(u'VOCA/Inputs_encoder/speech_features:0')
    condition_subject_id = graph.get_tensor_by_name(u'VOCA/Inputs_encoder/condition_subject_id:0')
    is_training = graph.get_tensor_by_name(u'VOCA/Inputs_encoder/is_training:0')
    input_template = graph.get_tensor_by_name(u'VOCA/Inputs_decoder/template_placeholder:0')
    output_decoder = graph.get_tensor_by_name(u'VOCA/output_decoder:0')

    num_frames = processed_audio.shape[0]
    feed_dict = {speech_features: np.expand_dims(np.stack(processed_audio), -1),
                 condition_subject_id: np.repeat(condition_idx-1, num_frames),
                 is_training: False,
                 input_template: np.repeat(template.v[np.newaxis, :, :, np.newaxis], num_frames, axis=0)}

    #with tf.Session() as session:
    with  tf.compat.v1.Session() as session:
        # Restore trained model
        saver.restore(session, tf_model_fname)
        predicted_vertices = np.squeeze(session.run(output_decoder, feed_dict))
        output_sequence_meshes(predicted_vertices, template, out_path)
    #tf.reset_default_graph()
    tf.compat.v1.reset_default_graph()
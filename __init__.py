bl_info = {
    "name": "Inference",
    "blender": (2, 80, 0),
    "category": "Object"
}

import bpy

import os
import glob
import argparse

import time

from . utils.inference import inference

from os import listdir
from contextlib import redirect_stdout
from pathlib import Path

class VOCAInference(bpy.types.Operator):
    """VOCA Inference"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.vocainference"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Inference"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def create_shapekeys(self): 
        directory = "./animation_output/meshes/"
        filepaths = [Path(directory, f) for f in listdir('./animation_output/meshes/')]
        filepaths.sort()

        print(filepaths)

        def import_obj(filepaths):
            with redirect_stdout(None):
                bpy.ops.import_scene.obj(filepath=filepaths, split_mode="OFF")
        
        def objtodefault(obj):     
            # imposta la posizione e la rotazione a default (0,0,0)
            obj.location = [0, 0, 0]
            obj.rotation_euler = [0, 0, 0] # faccia verso asse z

        # import first obj
        import_obj(str(filepaths[0]))
        # mette in primo piano la selezione (todo: guarda -1)
        main_obj = bpy.context.selected_objects[-1]
        objtodefault(main_obj)

        # todo: da vedere
        main_obj.shape_key_add(name=main_obj.name)
        # smoothing dell'oggetto
        for face in main_obj.data.polygons:
            face.use_smooth = True
        # todo: shape key con le varie mesh relative alla prima per ogni istante
        main_key = main_obj.data.shape_keys
        # attiva l'oggetto in primo piano
        bpy.context.view_layer.objects.active = main_obj
        seq_len = len(filepaths)
        
        # import the rest
        for i, filepath in enumerate(filepaths[1:]):
            import_obj(str(filepath))
            # mette in primo piano la selezione (todo: guarda -1)
            current_obj = bpy.context.selected_objects[-1]
            objtodefault(current_obj)

            # join as shapes (todo)
            # importa tutti gli oggetti e poi con join copia gli shape keys nel primo
            bpy.ops.object.join_shapes()

            # remove meshes
            #current_mesh = current_obj.data
            #current_mat = current_obj.material_slots[0].material
            bpy.data.objects.remove(current_obj, do_unlink=True)
            #bpy.data.meshes.remove(current_mesh, do_unlink=True)
            #bpy.data.materials.remove(current_mat, do_unlink=True)
        
        # set keyframes
        main_key.use_relative = True
        for i, key_block in enumerate(main_key.key_blocks[1:]):
            key_block.value = 0.0
            key_block.keyframe_insert("value", frame=i)
            key_block.value = 1.0
            key_block.keyframe_insert("value", frame=i+1)
            key_block.value = 0.0
            key_block.keyframe_insert("value", frame=i+2)

        # set start/end time
        bpy.context.scene.frame_start = 0
        bpy.context.scene.frame_end = seq_len - 1
        bpy.context.scene.frame_set(0)

    def add_audio(self, scene, audio_filepath): 
        #scene = bpy.context.scene
        scene.sequence_editor.sequences.new_sound("pippo", audio_filepath, 1, 0)

    def execute(self, context):        # execute() is called when running the operator.

        tf_model_fname = './model/gstep_52280.model'
        ds_fname =  './ds_graph/output_graph.pb'
        # audio_fname =  './audio/sentence20.wav'
        # audio_fname =  './audio/test_sentence.wav'
        audio_fname = './audio/loris-dick.wav'
        template_fname =  './template/FLAME_sample.ply'
        condition_idx =  3
        out_path =  './animation_output'
        
        print("Start inference")

        start_time = time.perf_counter()
        inference(tf_model_fname, 
                    ds_fname, 
                    audio_fname, 
                    template_fname, 
                    condition_idx, 
                    out_path)
        end_time = time.perf_counter()

        print("Mi piace il cazzo!\n")

        self.create_shapekeys()

        self.add_audio(context.scene, audio_fname)

        # set the camera
        context.scene.camera.rotation_euler = (0,0,0)
        context.scene.camera.location = (0, -0.02, 1.2)
 
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)

def menu_func(self, context):
    self.layout.operator(VOCAInference.bl_idname)

def register():
    bpy.utils.register_class(VOCAInference)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():   
    bpy.utils.unregister_class(VOCAInference)
    bpy.types.VIEW3D_MT_object.remove(menu_func) 


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
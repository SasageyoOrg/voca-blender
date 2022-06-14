
import bpy

from os import listdir
from contextlib import redirect_stdout
from pathlib import Path

import time

#from . utils.inference import inference

# RunVOCAOperator Class~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class RunVOCAOperator(bpy.types.Operator):
    """VOCA Inference"""                         # Use this as a tooltip for menu items and buttons.
    bl_idname = "opr.runvoca"                    # Unique identifier for buttons and menu items to reference.
    bl_label = "Run VOCA"                        # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}            # Enable undo for the operator.

    def execute(self, context):                  # execute() is called when running the operator.
         # get params by the panel
        path_voca = (
            context.scene.TemplatePath,
            context.scene.AudioPath,
            context.scene.OutputPath
        )
        (template_fname, audio_fname, out_path) =  path_voca

        # Standard VOCA's Path
        tf_model_fname = 'addon-source/model/gstep_52280.model'
        ds_fname =  'addon-source/ds_graph/output_graph.pb'
        condition_idx =  3

        print("INFERENZA")
        # Inference
        print("Start inference")

        start_time = time.perf_counter()
        # inference(tf_model_fname, 
        #             ds_fname, 
        #             audio_fname, 
        #             template_fname, 
        #             condition_idx, 
        #             out_path)
        # end_time = time.perf_counter()

        print("End inference!\n")
        print("Time: " + (end_time - start_time))

        # Call Import Meshes
        bpy.ops.opr.meshimport('EXEC_DEFAULT')
 
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# MeshImportOperator Class~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MeshImportOperator(bpy.types.Operator):
    """VOCA Inference"""                    # Use this as a tooltip for menu items and buttons.
    bl_idname = "opr.meshimport"            # Unique identifier for buttons and menu items to reference.
    bl_label = "Mesh Import"                # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}       # Enable undo for the operator.

    choice : bpy.props.BoolProperty(default = False)

    def create_shapekeys(self, directory): 
        #directory = directory + "/meshes"
        filepaths = [Path(directory, f) for f in listdir(directory)]
        filepaths.sort()

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

            # importa tutti gli oggetti e poi con join copia gli shape keys nel primo
            bpy.ops.object.join_shapes()

            # remove meshes
            bpy.data.objects.remove(current_obj, do_unlink=True)
        
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

        # Rename obj
        main_obj.name = "VOCA_mesh"

    def add_audio(self, scene, audio_filepath): 
        scene.sequence_editor.sequences.new_sound("audio", audio_filepath, 1, 0)        

    def execute(self, context):        
         # get params by the panel
        if self.choice:
            # params of import meshes pannel
            path_mesh = (
                context.scene.AudioPathMesh,
                context.scene.OutputPathMesh
            )
            (audio_fname, out_path) =  path_mesh  
        else:
            # params of run model pannel
            path_voca = (
                context.scene.TemplatePath,
                context.scene.AudioPath,
                context.scene.OutputPath
            )
            (_, audio_fname, out_path) =  path_voca

        print("IMPORT")
        # IMPORTING MESHES
        self.create_shapekeys(out_path)
        self.add_audio(context.scene, audio_fname)

        # set the camera
        context.scene.camera.rotation_euler = (0,0,0)
        context.scene.camera.location = (0, -0.02, 1.2)

        # set frame rate to 60 fps
        context.scene.render.fps = 60   
 
        return {'FINISHED'}                  
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
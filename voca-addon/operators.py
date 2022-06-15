import bpy
import sys
sys.tracebacklimit = -1
from bpy.types import Operator
from bpy.props import IntProperty

from os import listdir
from contextlib import redirect_stdout
from pathlib import Path

from . utils.inference import inference

# MAIN OPERATOR: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run model VOCA ============================
class Run_VOCA(Operator):
    """VOCA Inference"""                         # Use this as a tooltip for menu items and buttons.
    bl_idname = "opr.runvoca"                    # Unique identifier for buttons and menu items to reference.
    bl_label = "Run VOCA"                        # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}            # Enable undo for the operator.

    def execute(self, context):                  # execute() is called when running the operator.
        # get params by the panel
        path_voca = (
            context.scene.TemplatePath,
            context.scene.AudioPath,
            context.scene.OutputPath,
            context.scene.TextureObjPath,
            context.scene.TextureIMGPath,
            context.scene.Condition
        )
        (template_fname, audio_fname, out_path, uv_template_fname, texture_img_fname, condition_idx) =  path_voca

        # Standard VOCA's Path
        addondir = bpy.utils.user_resource('SCRIPTS', 'addons')
        tf_model_fname = addondir + '/voca-addon/model/gstep_52280.model'
        ds_fname =  addondir + '/voca-addon/ds_graph/output_graph.pb'

        # Inference
        print("Start inference")
        try:
            inference(tf_model_fname, 
                        ds_fname, 
                        audio_fname, 
                        template_fname, 
                        condition_idx, 
                        uv_template_fname,
                        texture_img_fname,
                        out_path)
        except Exception as e:
            self.report({"ERROR"}, ("Errore: " + str(e)))
            return {"CANCELLED"}
        print("End inference\n")

        # Call Import Meshes
        try:
            bpy.ops.opr.meshimport('EXEC_DEFAULT')
        except Exception as e:
            self.report({"ERROR"}, ("Errore: " + str(e)))
 
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.
# ===========================================

# Import Meshes =============================
class Mesh_Import(Operator):
    """VOCA Inference"""                    # Use this as a tooltip for menu items and buttons.
    bl_idname = "opr.meshimport"            # Unique identifier for buttons and menu items to reference.
    bl_label = "Mesh Import"                # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}       # Enable undo for the operator.

    choice : IntProperty(default = 1)

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
        if self.choice == 1:
            # params of import meshes pannel
            path_mesh = (
                context.scene.AudioPathMesh,
                context.scene.MeshPath
            )
            (audio_fname, out_path) =  path_mesh  
        elif self.choice == 2:
            # params of run model pannel
            path_voca = (
                # context.scene.TemplatePath,
                context.scene.AudioPath,
                context.scene.OutputPath
            )
            # (_, audio_fname, out_path) =  path_voca
            (audio_fname, out_path) =  path_voca
            out_path = out_path + 'meshes/'
        elif self.choice == 3:
            # params of run model pannel
            path_edit = (
                # context.scene.TemplatePath,
                context.scene.AudioPath_edit,
                context.scene.OutputPath_edit
            )
            (audio_fname, out_path) =  path_edit
            out_path = out_path + 'meshes/'

        print("IMPORT")
        # IMPORTING MESHES
        try:
            self.create_shapekeys(out_path)
            self.add_audio(context.scene, audio_fname)
        except Exception as e:
            self.report({"ERROR"}, ("Errore: " + str(e)))
        # set the camera
        context.scene.camera.rotation_euler = (0,0,0)
        context.scene.camera.location = (0, -0.02, 1.2)

        # set the camera
        context.scene.camera.rotation_euler = (0,0,0)
        context.scene.camera.location = (0, -0.02, 1.2)

        # set frame rate to 60 fps
        context.scene.render.fps = 60   
 
        return {'FINISHED'}                  
# ===========================================

# Edit Meshes VOCA ============================
class Mesh_Edit(Operator):
    """VOCA Inference"""                         # Use this as a tooltip for menu items and buttons.
    bl_idname = "opr.meshedit"                   # Unique identifier for buttons and menu items to reference.
    bl_label = "Mesh Edit"                       # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}            # Enable undo for the operator.

    def execute(self, context):                  # execute() is called when running the operator.
        # get params by the panel
        path_edit = (
            context.scene.SourceMeshPath_edit,
            context.scene.OutputPath_edit,
            context.scene.TempletePath_edit,
            context.scene.AudioPath_edit,
            context.scene.DropdownChoice
        )
        (source_path, out_path, flame_model_path, _, mode) =  path_edit
        mode_edit = (
            context.scene.n_blink,
            context.scene.duration_blink,
            context.scene.index_shape,
            context.scene.maxVariation_shape,
            context.scene.index_pose,
            context.scene.maxVariation_pose
        )
        if mode == 'Blink':
            (param_a, param_b, _, _, _, _) =  mode_edit
        elif mode == 'Shape':
            (_, _, param_a, param_b, _, _) =  mode_edit
        elif mode == 'Pose':
            (_, _, _, _, param_a, param_b) =  mode_edit

        # Inference
        print("Start edit")

        # edit(source_path, 
        #     out_path, 
        #     flame_model_path, 
        #     mode,
        #     param_a,
        #     param_b) 
        
        print("End edit\n")

        try:
            # Call Import Meshes
            bpy.ops.opr.meshimport('EXEC_DEFAULT', choice = 3)
        except Exception as e:
            self.report({"ERROR"}, ("Errore: " + str(e)))
 
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.
# ===========================================
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# HANDLE MESHES OPERATORS: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DELETE ALL MESHES ========================================
class Mesh_Delete(Operator):
    bl_idname = 'object.delete_meshes'
    bl_label = 'Delete meshes'
    bl_description = 'Delete all meshes'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj.select_set(True)
                bpy.ops.object.delete()
        return {'FINISHED'}

# DELETE OTHER MESHES ========================================
class Mesh_Delete_Other(Operator):
    bl_idname = 'object.delete_other_meshes'
    bl_label = 'Delete other meshes'
    bl_description = 'Delete all other meshes'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            print(obj.name)
            if obj.type == 'MESH' and (not "VOCA" in obj.name):
                obj.select_set(True)
                bpy.ops.object.delete()
        return {'FINISHED'}
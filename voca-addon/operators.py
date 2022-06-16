import bpy
from bpy.types import Operator
from bpy.props import IntProperty

from os import listdir
from contextlib import redirect_stdout
from pathlib import Path

from . utils.inference import inference
from . utils.edit_sequences import add_eye_blink
from . utils.edit_sequences import alter_sequence_shape
from . utils.edit_sequences import alter_sequence_head_pose

# MAIN OPERATOR: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run model VOCA ============================
class Run_VOCA(Operator):
    """VOCA Inference"""                         # Use this as a tooltip for menu items and buttons.
    bl_idname = "opr.runvoca"                    # Unique identifier for buttons and menu items to reference.
    bl_label = "Run VOCA"                        # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}            # Enable undo for the operator.

    def execute(self, context):                  # execute() is called when running the operator.
        # get params by the panel
        (template_fname, audio_fname, out_path, uv_template_fname, texture_img_fname, condition_idx) = (
            context.scene.TemplatePath,
            context.scene.AudioPath,
            context.scene.OutputPath,
            context.scene.TextureObjPath,
            context.scene.TextureIMGPath,
            context.scene.Condition
        )

        # Standard VOCA's Path
        addondir = bpy.utils.user_resource('SCRIPTS', 'addons')
        tf_model_fname = addondir + '/voca-addon/model/gstep_52280.model'
        ds_fname =  addondir + '/voca-addon/ds_graph/output_graph.pb'

        # Inference
        print("Start inference")        

        inference(tf_model_fname, 
                    ds_fname, 
                    audio_fname, 
                    template_fname, 
                    condition_idx, 
                    uv_template_fname,
                    texture_img_fname,
                    out_path)
        
        print("End inference\n")

        # Call Import Meshes
        bpy.ops.opr.meshimport('EXEC_DEFAULT', choice = 2)
 
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
        name_audio = 'VOCA_' + (audio_filepath.rsplit("/")[-1])
        scene.sequence_editor.sequences.new_sound(name_audio, audio_filepath, 1, 0)

    def execute(self, context):        
        if self.choice == 1:
            # params of IMPORT MESHES PANEL
            (audio_fname, out_path) = (
                context.scene.AudioPathMesh,
                context.scene.MeshPath
            )
            self.add_audio(context.scene, audio_fname)  
        elif self.choice == 2:
            # params of RUN MODEL PANL
            (audio_fname, out_path) = (
                context.scene.AudioPath,
                (context.scene.OutputPath + 'meshes/')
            )
            self.add_audio(context.scene, audio_fname)
        elif self.choice == 3:
            # params of EDIT PANEL
            (audio_fname, out_path) = (
                context.scene.AudioPath_edit,
                (context.scene.OutputPath_edit + 'meshes/')
            )
            
            list_sounds = context.scene.sequence_editor.sequences
            cond = any('VOCA' in strip.name for strip in list_sounds)
            if not cond:
                self.add_audio(context.scene, audio_fname)

        print("IMPORT\n")
        # IMPORTING MESHES
        self.create_shapekeys(out_path)

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
        (source_path, out_path, flame_model_path, mode, uv_template_fname, texture_img_fname) = (
            context.scene.SourceMeshPath_edit,
            context.scene.OutputPath_edit,
            context.scene.FlameModelPath_edit,
            context.scene.DropdownChoice,
            context.scene.TextureObjPath_edit,
            context.scene.TextureIMGPath_edit,
        )

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
            add_eye_blink(source_path, out_path, flame_model_path, param_a, param_b, uv_template_fname=uv_template_fname, texture_img_fname=texture_img_fname)
        elif mode == 'Shape':
            (_, _, param_a, param_b, _, _) =  mode_edit
            alter_sequence_shape(source_path, out_path, flame_model_path, pc_idx=param_a, pc_range=(0,param_b), uv_template_fname=uv_template_fname, texture_img_fname=texture_img_fname)
        elif mode == 'Pose':
            (_, _, _, _, param_a, param_b) =  mode_edit
            alter_sequence_head_pose(source_path, out_path, flame_model_path, pose_idx=param_a, rot_angle=param_b, uv_template_fname=uv_template_fname, texture_img_fname=texture_img_fname)

        # Call Import Meshes
        bpy.ops.opr.meshimport('EXEC_DEFAULT', choice = 3)
 
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
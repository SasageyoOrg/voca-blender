# ---------------------------------------------------------------------------- #
#                                Module imports                                #
# ---------------------------------------------------------------------------- #

import bpy
import re
from curses import panel
from math import pi
from bpy.types import Panel
from bpy.props import ( StringProperty,
                        BoolProperty,
                        IntProperty,
                        FloatProperty,
                        EnumProperty,
                        )

# ---------------------------------------------------------------------------- #
#                              Props and callbacks                             #
# ---------------------------------------------------------------------------- #

PROPS = { 
         # -------------------------------- Main props -------------------------------- #
    'RUN': [
        ('TemplatePath', StringProperty(name = "", default = "path_to_template.ply", description = "Define the root path of the Template", subtype = 'FILE_PATH')),
        ('AudioPath', StringProperty(name = "", default = "path_to_audio.wav", description = "Define the root path of the Audio", subtype = 'FILE_PATH')),
        ('OutputPath', StringProperty(name = "", default = "path_to_output_meshes/", description = "Define the root path of the Output", subtype = 'DIR_PATH')),
        ('Condition', IntProperty(name = "", default = 3, description = "facial expression", min = 0, max = 8))
    ],
    'TEXTURE_RUN':[
        ('AddTexture', BoolProperty(name = 'Add Texture', default = False)),
        ('TextureObjPath', StringProperty(name = "", default = "path_to_OBJ/", description = "Define the root path of the OBJ texture", subtype = 'FILE_PATH')),
        ('TextureIMGPath', StringProperty(name = "", default = "path_to_IMG/", description = "Define the root path of the IMG texture", subtype = 'FILE_PATH'))
    ],
    'MESH' : [
        ('AudioPathMesh', StringProperty(name = "", default = "path_to_audio.wav", description = "Define the root path of the Audio", subtype = 'FILE_PATH')),
        ('MeshPath', StringProperty(name = "", default = "path_to_meshes/", description = "Define the root path of the Output", subtype = 'DIR_PATH'))
    ],
    # -------------------------------- Edit props -------------------------------- #
    'EDIT':[
        ('SourceMeshPath_edit', StringProperty(name = "", default = "path_to_source_meshes/", description = "Define the root path of the Source", subtype = 'DIR_PATH')),
        ('OutputPath_edit', StringProperty(name = "", default = "path_to_output_edited/", description = "Define the root path of the Output", subtype = 'DIR_PATH')),
        ('FlameModelPath_edit', StringProperty(name = "", default = "path_to_model.pkl", description = "Define the path of the FLAME model", subtype = 'FILE_PATH')),
        ('AudioPath_edit', StringProperty(name = "", default = "path_to_audio.wav", description = "Define the root path of the Audio", subtype = 'FILE_PATH')),
        ('DropdownChoice', EnumProperty(
            items=(
                ("Blink", "Blink", "Tooltip for Blink"),
                ("Shape", "Shape", "Tooltip for Shape"),
                ("Pose", "Pose", "Tooltip for Pose"),
            ),
            name = "Edit",
            default = "Blink",
            description = "Dropdown to choice edit mode"))
    ],
    'BLINK':[
        ('n_blink', IntProperty(name = "Number", default = 2, description = "Define the root path of the Output", min = 0, max = 100)),
        ('duration_blink', IntProperty(name = "Duration", default = 15, description = "Define the root path of the Output", min = 5, max = 30))
    ],
    'SHAPE':[
        ('index_shape', IntProperty(name = "Index", default = 0, description = "", min = 0, max = 299)),
        ('maxVariation_shape', IntProperty(name = "Max Variation", default = 3, description = "", min = 0, max = 3))
    ],
    'POSE':[
        ('index_pose', IntProperty(name = "Index", default = 3, description = "", min = 3, max = 5)),
        ('maxVariation_pose', FloatProperty(name = "Max Variation", default = 0.52, description = "", min = 0.0, max = (2*pi - 0.01)))
    ],
    'TEXTURE_EDIT':[
        ('AddTexture_edit', BoolProperty(name = 'Add Texture', default = False)),
        ('TextureObjPath_edit', StringProperty(name = "", default = "path_to_OBJ/", description = "Define the root path of the OBJ texture", subtype = 'FILE_PATH')),
        ('TextureIMGPath_edit', StringProperty(name = "", default = "path_to_IMG/", description = "Define the root path of the IMG texture", subtype = 'FILE_PATH'))
    ],
    # -------------------------------- Other props ------------------------------- #
    'HIDE': [('hide', BoolProperty(name="Hide meshes", description="Check-box to hide no-VOCA meshes", default=False, update=hide_callback))]
}

def loadUI_w_label(scene, name, box):
    row = box.row()
    # add space on var name
    name_string = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', name).replace('_edit','').replace(' Path','')
    row.label(text = name_string + ': ')
    row = box.row()
    row.prop(scene, name)

def loadUI_no_label(scene, box, props, check, choice_texture):
    for (prop_name, _) in props:
        row = box.row()
        # Disable row if not checked
        if prop_name != check:
            row = row.row()
            row.enabled = choice_texture
        row.prop(scene, prop_name)


def hide_callback(self, context):
    for obj in bpy.context.blend_data.objects:
        if obj.type == 'MESH' and (not "VOCA" in obj.name):
            obj.hide_viewport = context.scene.hide

# ---------------------------------------------------------------------------- #
#                                    Panels                                    #
# ---------------------------------------------------------------------------- #

# ------------------------------ Run Voca panel ------------------------------ #
class run_model_panel(Panel):
    bl_idname = "VOCA_PT_run_model"
    bl_label = 'Run VOCA Model'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VOCA'
    # bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout

        box = layout.box()
        for (prop_name, _) in PROPS['RUN']:
            loadUI_w_label(context.scene, prop_name, box)
        
        # Texture
        box = layout.box()
        choice_texture = context.scene.AddTexture
        loadUI_no_label(context.scene, box, PROPS['TEXTURE_RUN'], 'AddTexture', choice_texture)

        col = self.layout.column()
        col.operator('opr.runvoca', text='Run')

# ---------------------------- Import meshes panel --------------------------- #
class mesh_import_panel(Panel):
    bl_idname = "VOCA_PT_mesh_import"
    bl_label = 'Import Mesh'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VOCA'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout

        box = layout.box()
        for (prop_name, _) in PROPS['MESH']:
            loadUI_w_label(context.scene, prop_name, box)

        col = self.layout.column()
        col.operator('opr.meshimport', text='Import')

# --------------------------------- Dev Panel -------------------------------- #
class dev_pannel(Panel):
    bl_idname = "VOCA_PT_dev_obj"
    bl_label = 'Dev'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VOCA'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        col = self.layout.column()
        row = col.row(align=True)

        # ----------------------------- Clean options box ---------------------------- #
        box = layout.box()
        row = box.row()
        row.prop(context.scene, PROPS['HIDE'][0][0], text="Hide non-VOCA meshes")
        row = box.row()
        row.enabled = not(context.scene.hide)
        row.operator("object.delete_other_meshes", text="Delete non-VOCA Object")
        row = box.row()
        row.operator("object.delete_meshes", text="Delete ALL Object")

        # ------------------------------ Edit meshes box ----------------------------- #
        # add path UI
        box_edit = layout.box()
        box = box_edit.box()
        for (prop_name, _) in PROPS['EDIT'][0:3]:
            loadUI_w_label(context.scene, prop_name, box)
        
        # Check if exists sound that have substring VOCA_
        # if there aren't, show prop. for path audio edit
        list_sounds = context.scene.sequence_editor.sequences
        cond = any('VOCA' in strip.name for strip in list_sounds)
        if not cond:
            box = box_edit.box()
            loadUI_w_label(context.scene, PROPS['EDIT'][3][0], box)
        
        # ------------------------------- Add mode box ------------------------------- #
        box = box_edit.box()
        row = box.row()
        row.prop(context.scene, PROPS['EDIT'][4][0])
        mode = context.scene.DropdownChoice
        loadUI_no_label(context.scene, box, PROPS[mode.upper()], '', True)

        # --------------------------- Texture settings box --------------------------- #
        box = box_edit.box()
        choice_texture = context.scene.AddTexture_edit
        loadUI_no_label(context.scene, box, PROPS['TEXTURE_EDIT'], 'AddTexture_edit', choice_texture)

        # col = self.layout.column()
        col = box_edit.column()
        col.operator('opr.meshedit', text='Run')

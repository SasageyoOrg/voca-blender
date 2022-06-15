import bpy
from math import pi
from bpy.types import Panel
from bpy.props import ( StringProperty,
                        BoolProperty,
                        IntProperty,
                        FloatProperty,
                        EnumProperty,
                    )

import re

def hide_callback(self, context):
    #print(bpy.types.Scene)
    for obj in bpy.context.blend_data.objects:
        if obj.type == 'MESH' and (not "VOCA" in obj.name):
            obj.hide_viewport = context.scene.hide
            
PROPS = { 
    'MENU': [
        ('TemplatePath', StringProperty(name = "", default = "template.ply", description = "Define the root path of the Template", subtype = 'FILE_PATH')),
        ('AudioPath', StringProperty(name = "", default = "audio.wav", description = "Define the root path of the Audio", subtype = 'FILE_PATH')),
        ('OutputPath', StringProperty(name = "", default = "path_to_output_meshes/", description = "Define the root path of the Output", subtype = 'DIR_PATH')),
        ('Condition', IntProperty(name = "", default = 3, description = "facial expression", min = 0, max = 8))
    ],
    'TEXTURE':[
        ('AddTexture', BoolProperty(name = 'Add Texture', default = False)),
        ('TextureObjPath', StringProperty(name = "", default = "path_to_OBJ_texture/", description = "Define the root path of the OBJ texture", subtype = 'FILE_PATH')),
        ('TextureIMGPath', StringProperty(name = "", default = "path_to_IMG_texture/", description = "Define the root path of the IMG texture", subtype = 'FILE_PATH'))
    ],
    'MESH' : [
        ('AudioPathMesh', StringProperty(name = "", default = "audio.wav", description = "Define the root path of the Audio", subtype = 'FILE_PATH')),
        ('MeshPath', StringProperty(name = "", default = "path_to_meshes_import/", description = "Define the root path of the Output", subtype = 'DIR_PATH'))
    ],
    'EDIT':[
        ('SourceMeshPath_edit', StringProperty(name = "", default = "path_to_source_meshes/", description = "Define the root path of the Source", subtype = 'DIR_PATH')),
        ('OutputPath_edit', StringProperty(name = "", default = "path_to_output_edited/", description = "Define the root path of the Output", subtype = 'DIR_PATH')),
        ('FlameModelPath_edit', StringProperty(name = "", default = "generic_model.pkl", description = "Define the path of the FLAME model", subtype = 'FILE_PATH')),
        ('AudioPath_edit', StringProperty(name = "", default = "audio.wav", description = "Define the root path of the Audio", subtype = 'FILE_PATH')),
        ('DropdownChoice', EnumProperty(
            items=(
                ("Blink", "Blink", "Tooltip for Blink"),
                ("Shape", "Shape", "Tooltip for Shape"),
                ("Pose", "Pose", "Tooltip for Pose"),
            ),
            name = "Edit mode",
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
    'HIDE': [('hide', BoolProperty(name="Hide meshes", description="Check-box to hide no-VOCA meshes", default=False, update=hide_callback))]
}

# RUN VOCA ==================================
class run_model_panel(Panel):
    bl_idname = "VOCA_PT_run_model"
    bl_label = 'Run VOCA Model'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VOCA'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout

        box = layout.box()
        for (prop_name, _) in PROPS['MENU']:
            row = box.row()
            # add space on var name
            name_string = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', prop_name)
            row.label(text = name_string + ': ')
            row = box.row()
            row.prop(context.scene, prop_name)
        
        # Texture
        box = layout.box()
        for (prop_name, _) in PROPS['TEXTURE']:
            row = box.row()
            # Disable row if not checked
            if prop_name != 'AddTexture':
                row = row.row()
                row.enabled = context.scene.AddTexture
            row.prop(context.scene, prop_name)

        col = self.layout.column()
        col.operator('opr.runvoca', text='Run')
# ===========================================

# IMPORTING MESHES ==========================
class mesh_import_panel(Panel):
    bl_idname = "VOCA_PT_mesh_import"
    bl_label = 'Import Mesh'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VOCA'
    bl_options = {'DEFAULT_CLOSED'}

    choice_opr = 'Mesh'
    
    def draw(self, context):
        layout = self.layout

        box = layout.box()
        for (prop_name, _) in PROPS['MESH']:
            row = box.row()
            # add space on var name
            name_string = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', prop_name)
            row.label(text = name_string + ': ')
            row = box.row()
            row.prop(context.scene, prop_name)

        col = self.layout.column()
        col.operator('opr.meshimport', text='Import')
# ===========================================

# EDIT MESHES ============================
class edit_mesh_panel(Panel):
    bl_idname = "VOCA_PT_Edit_Meshes"
    bl_label = 'Edit Meshes'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VOCA'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout

        # add path UI
        box = layout.box()
        for (prop_name, _) in PROPS['EDIT'][0:4]:
            row = box.row()
            # add space on var name
            name_string = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', prop_name)
            name_string = name_string.replace('_edit','')
            row.label(text = name_string + ': ')
            row = box.row()
            row.prop(context.scene, prop_name)
        
        # add mode UI
        box = layout.box()
        row = box.row()
        row.prop(context.scene, PROPS['EDIT'][4][0])
        mode = context.scene.DropdownChoice
        for (prop_name, _) in PROPS[mode.upper()]:
            row = box.row()
            row.prop(context.scene, prop_name)

        col = self.layout.column()
        col.operator('opr.meshedit', text='Run')
# ===========================================


# CLEAR & DELETE PANEL ======================
class clear_pannel(Panel):
    bl_idname = "VOCA_PT_Clear_obj"
    bl_label = 'Dev'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VOCA'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        col = self.layout.column()
        row = col.row(align=True)

        box = layout.box()
        row = box.row()
        row.prop(context.scene, PROPS['HIDE'][0][0], text="Hide non-VOCA meshes")
        
        row = box.row()
        row.enabled = not(context.scene.hide)
        row.operator("object.delete_meshes", text="Delete ALL Object")

        row = box.row()
        row.operator("object.delete_other_meshes", text="Delete non-VOCA Object")
# ===========================================
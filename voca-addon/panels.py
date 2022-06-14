import bpy
from bpy.types import Panel
from bpy.props import (StringProperty,
                       BoolProperty,
                    #    IntProperty,
                    #    FloatProperty,
                    #    FloatVectorProperty,
                    #    EnumProperty,
                    #    PointerProperty,
                       )

PROPS = { 
    'MENU': [
        ('TemplatePath', StringProperty(name = "", default = "template.ply", description = "Define the root path of the Template", subtype = 'FILE_PATH')),
        ('AudioPath', StringProperty(name = "", default = "audio.wav", description = "Define the root path of the Audio", subtype = 'FILE_PATH')),
        ('OutputPath', StringProperty(name = "", default = "path_to_output_meshes/", description = "Define the root path of the Output", subtype = 'DIR_PATH'))
    ],
    'MESH' : [
        ('AudioPathMesh', StringProperty(name = "", default = "audio.wav", description = "Define the root path of the Audio", subtype = 'FILE_PATH')),
        ('OutputPathMesh', StringProperty(name = "", default = "path_to_meshes_import/", description = "Define the root path of the Output", subtype = 'DIR_PATH'))
    ]
}

# RUN VOCA ==================================
class run_model_panel(Panel):
    bl_idname = "VOCA_PT_run_model"
    bl_label = 'Run VOCA Model'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VOCA'
    
    def draw(self, context):
        layout = self.layout

        for (prop_name, _) in PROPS['MENU']:
            box = layout.box()
            row = box.row()
            row.label(text = prop_name + ': ')
            row = box.row()
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

        for (prop_name, _) in PROPS['MESH']:
            box = layout.box()
            row = box.row()
            row.label(text = prop_name + ': ')
            row = box.row()
            row.prop(context.scene, prop_name)

        col = self.layout.column()
        col.operator('opr.meshimport', text='Import').choice = True
# ===========================================

# CLEAR & DELETE PANEL ======================
class handle_meshes_panel(Panel):  
    bl_idname = "VOCA_PT_handle_meshes"
    bl_label = 'Clear Objects'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VOCA'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        #self.layout.label(text='Clear Object')
        col = self.layout.column()
        col.operator("object.hide_viewport_clear", text="Hide Object")
        col.operator("object.delete_meshes", text="Delete ALL Object")
        col.operator("object.delete_other_meshes", text="Delete no-VOCA Object")
# ===========================================

# TODO: setup installation
# class SetupPanel(bpy.types.Panel):
#     bl_idname = "VOCA_pannel_setup"
#     bl_label = 'Setup'
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'VOCA'
    
#     def draw(self, context):
#         self.layout.label(text='Setup')
        
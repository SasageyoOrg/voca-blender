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


def hide_callback(self, context):
    print(bpy.types.Scene)
    for obj in bpy.context.blend_data.objects:
        if obj.type == 'MESH' and (not "VOCA" in obj.name):
            obj.hide_viewport = context.scene.hide
            
PROPS = { 
    'MENU': [
        ('TemplatePath', StringProperty(name = "", default = "template.ply", description = "Define the root path of the Template", subtype = 'FILE_PATH')),
        ('AudioPath', StringProperty(name = "", default = "audio.wav", description = "Define the root path of the Audio", subtype = 'FILE_PATH')),
        ('OutputPath', StringProperty(name = "", default = "meshes_output_dir/", description = "Define the root path of the Output", subtype = 'DIR_PATH'))
    ],
    'MESH' : [
        ('AudioPathMesh', StringProperty(name = "", default = "addon-source/audio/test_sentence.wav", description = "Define the root path of the Audio", subtype = 'FILE_PATH')),
        ('OutputPathMesh', StringProperty(name = "", default = "addon-source/animation_output/meshes/", description = "Define the root path of the Output", subtype = 'DIR_PATH'))
    ],
    'HIDE': [('hide', BoolProperty(name="Hide meshes", description="Some tooltip", default=False, update=hide_callback))]
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



# CLEAR & DELETE PANEL


class ClearPanel(bpy.types.Panel):
    bl_idname = "clear_objects"
    bl_label = 'Clear Objects'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VOCA'

    @classmethod
    def pool(cls, context):
        return False
    
    def draw(self, context):
        layout = self.layout
        col = self.layout.column()
        row = col.row(align=True)
        #Checkbox Here
        row.prop(context.scene, PROPS['HIDE'][0][0], text="Hide non-VOCA meshes")
        col.operator("object.delete_meshes", text="Delete ALL Object")
        col.operator("object.delete_other_meshes",
                     text="Delete non-VOCA Object")


# TODO: setup installation
# class SetupPanel(bpy.types.Panel):
#     bl_idname = "VOCA_pannel_setup"
#     bl_label = 'Setup'
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'VOCA'
    
#     def draw(self, context):
#         self.layout.label(text='Setup')
        
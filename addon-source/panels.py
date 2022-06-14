import bpy

PROPS = { 
    'MENU': [
        ('TemplatePath', bpy.props.StringProperty(name = "", default = "addon-source/model/gstep_52280.model", description = "Define the root path of the Template", subtype = 'DIR_PATH')),
        ('AudioPath', bpy.props.StringProperty(name = "", default = "addon-source/audio/test_sentence.wav", description = "Define the root path of the Audio", subtype = 'DIR_PATH')),
        ('OutputPath', bpy.props.StringProperty(name = "", default = "addon-source/animation_output", description = "Define the root path of the Output", subtype = 'DIR_PATH'))
    ],
    'MESH' : [
        ('AudioPathMesh', bpy.props.StringProperty(name = "", default = "addon-source/audio/test_sentence.wav", description = "Define the root path of the Audio", subtype = 'DIR_PATH')),
        ('OutputPathMesh', bpy.props.StringProperty(name = "", default = "addon-source/animation_output/meshes/", description = "Define the root path of the Output", subtype = 'DIR_PATH'))
    ]
}

class MenuPanel(bpy.types.Panel):
    
    bl_idname = "VOCA_pannel_menu"
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

class MeshPanel(bpy.types.Panel):
    
    bl_idname = "VOCA_pannel_mesh"
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


# class SetupPanel(bpy.types.Panel):
    
#     bl_idname = "VOCA_pannel_setup"
#     bl_label = 'Setup'
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'VOCA'
    
#     def draw(self, context):
#         self.layout.label(text='Setup')
        
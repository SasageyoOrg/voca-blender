import bpy

class MenuPanel(bpy.types.Panel):
    
    bl_idname = "VOCA_pannel_menu"
    bl_label = 'Menu'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VOCA'
    
    def draw(self, context):
        self.layout.label(text='Mi piace il Cazzo')

class SetupPanel(bpy.types.Panel):
    
    bl_idname = "VOCA_pannel_setup"
    bl_label = 'Setup'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VOCA'
    
    def draw(self, context):
        self.layout.label(text='Mi piace il Cazzo  grosso e nero')
        
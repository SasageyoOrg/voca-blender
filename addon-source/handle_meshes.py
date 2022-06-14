import bpy
from bpy.types import Operator
 
# HIDE ALL MESHES ========================================  
class OBJECT_hide_viewport_clear(Operator):
    bl_idname = 'object.hide_viewport_clear'
    bl_label = 'Clear viewport hide'
    bl_description = 'Globally cler hiding in viewport'
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        for obj in context.blend_data.objects:
            if obj.type == 'MESH' and (not "VOCA" in obj.name):
                if obj.hide_viewport == False:
                    obj.hide_viewport = True
                else:
                    obj.hide_viewport = False   
        return {'FINISHED'}
    
# DELETE ALL MESHES ========================================   
class mesh_delete(Operator):
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
class mesh_delete_other(Operator):
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
    
# CLEAR & DELETE PANEL
class ClearPanel(bpy.types.Panel):  
    bl_idname = "clear_objects"
    bl_label = 'Clear Objects'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VOCA'
    
    def draw(self, context):
        #self.layout.label(text='Clear Object')
        col = self.layout.column()
        col.operator("object.hide_viewport_clear", text="Hide Object")
        col.operator("object.delete_meshes", text="Delete ALL Object")
        col.operator("object.delete_other_meshes", text="Delete no-VOCA Object")
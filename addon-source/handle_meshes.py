import bpy
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
 
 
class OBJECT_hide_viewport(Operator):
    bl_idname = 'object.hide_viewport'
    bl_label = 'Hide viewport'
    bl_description = 'Globally disable in viewport'
    bl_options = {'REGISTER', 'UNDO'}
 
    def execute(self, context):
        for obj in context.selected_objects:
            obj.hide_viewport = True
        return {'FINISHED'}
    
    
    
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
    
    bl_idname = "clear objects"
    bl_label = 'clear objects'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VOCA'
    
    def draw(self, context):
        self.layout.label(text='Mi piace il Cazzo  grosso e nero')
        col = self.layout.column()
        col.operator("object.hide_viewport_clear", text="Nascondi gli altri oggetti")
        col.operator("object.delete_meshes", text="Elimina tutte le mesh")
        col.operator("object.delete_other_meshes", text="Elimina le mesh non VOCA")
        
        
        
def register():
    register_class(OBJECT_hide_viewport_clear)
    register_class(ClearPanel)
    register_class(mesh_delete)
    register_class(mesh_delete_other)
 
def unregister():
    unregister_class(OBJECT_hide_viewport_clear)
    unregister_class(ClearPanel)
    unregister_class(mesh_delete)
    unregister_class(mesh_delete_other)
    
 
if __name__ == '__main__':
    register()
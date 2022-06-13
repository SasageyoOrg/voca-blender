bl_info = {
    "name": "Inference",
    "blender": (2, 80, 0),
    "category": "Object"
}


from inspect import _void
import bpy
import os
import glob
import argparse
import time
from . utils.inference import inference


from pathlib import Path
from bpy.props import (
    BoolProperty,
    CollectionProperty,
    StringProperty,
)
from bpy_extras.io_utils import ImportHelper


from os import listdir
from os.path import isfile, join
from contextlib import redirect_stdout


class VOCAInference(bpy.types.Operator):
    """VOCA Inference"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.vocainference"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Inference"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    

    def execute(self, context):        # execute() is called when running the operator.
        
        self.create_shapekeys()

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.


    

def menu_func(self, context):
    self.layout.operator(VOCAInference.bl_idname)

def register():
    bpy.utils.register_class(VOCAInference)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():   
    bpy.utils.unregister_class(VOCAInference)
    bpy.types.VIEW3D_MT_object.remove(menu_func) 


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
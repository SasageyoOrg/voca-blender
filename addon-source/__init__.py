bl_info = {
    "name": "VOCA Add-On",
    "author": "Sasageyo",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "Add-on for voca model",
    "warning": "",
    "doc_url": "",
    "category": "VOCA",
}

import bpy

from os import listdir

from . panels import MenuPanel, MeshPanel
from . handle_meshes import OBJECT_hide_viewport_clear, ClearPanel, mesh_delete, mesh_delete_other
from . main_operator import RunVOCAOperator, MeshImportOperator

# GLOBAL Var ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CLASSES = [
    RunVOCAOperator,
    MeshImportOperator,
    MenuPanel,
    MeshPanel,
    OBJECT_hide_viewport_clear,
    ClearPanel,
    mesh_delete,
    mesh_delete_other
]

PROPS = panels.PROPS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ADD-ON func ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def register():
    for PROP in PROPS.values():
        for (prop_name, prop_value) in PROP:
            setattr(bpy.types.Scene, prop_name, prop_value)

    for klass in CLASSES:
        bpy.utils.register_class(klass)

def unregister():  
    for PROP in PROPS.values():
        for (prop_name, prop_value) in PROP:
            delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)

if __name__ == "__main__":
    register()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

from . panels import run_model_panel, mesh_import_panel, handle_meshes_panel
from . operators import Run_VOCA, Mesh_Import, Mesh_Hide, Mesh_Delete_All, Mesh_Delete_Other

# GLOBAL Var ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CLASSES = [
    Run_VOCA,
    Mesh_Import,
    run_model_panel,
    mesh_import_panel,
    Mesh_Hide,
    handle_meshes_panel,
    Mesh_Delete_All,
    Mesh_Delete_Other
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

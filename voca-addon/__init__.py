
from . panels import run_model_panel, mesh_import_panel, clear_pannel, edit_mesh_panel
from . operators import Run_VOCA, Mesh_Import, Mesh_Edit, Mesh_Delete, Mesh_Delete_Other
bl_info = {
    "name": "VOCA Add-On",
    "author": "Sasageyo",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "Add-on for voca framework",
    "warning": "",
    "doc_url": "",
    "category": "VOCA",
}

import bpy

# GLOBAL Var ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CLASSES = [
    Run_VOCA,
    Mesh_Import,
    Mesh_Edit,
    run_model_panel,
    mesh_import_panel,
    edit_mesh_panel,
    Mesh_Delete,
    Mesh_Delete_Other,
    clear_pannel
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
    # bpy.types.Scene.hide = bpy.props.BoolProperty(
    #     name="Hide meshes",
    #     description="Some tooltip",
    #     default=False)

def unregister():  
    for PROP in PROPS.values():
        for (prop_name, prop_value) in PROP:
            delattr(bpy.types.Scene, prop_name)

    for klass in CLASSES:
        bpy.utils.unregister_class(klass)
    # del bpy.types.Scene.my_prop

if __name__ == "__main__":
    register()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

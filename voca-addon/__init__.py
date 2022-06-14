
from . panels import run_model_panel, mesh_import_panel, ClearPanel
from . operators import Run_VOCA, Mesh_Import, MeshDelete, MeshDeleteOther
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
    run_model_panel,
    mesh_import_panel,
    MeshDeleteOther,
    MeshDelete,
    ClearPanel
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

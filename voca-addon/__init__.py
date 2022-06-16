bl_info = {
    "name": "VOCA Add-On",
    "author": "Sasageyo",
    "version": (1, 0, 0),
    "blender": (2, 92, 0),
    "location": "View3D",
    "description": "Add-on for voca framework",
    "warning": "Requires installation of dependencies",
    "doc_url": "",
    "category": "VOCA",
}

import bpy
import os
import sys
import subprocess
import importlib
import shutil
from collections import namedtuple
from sys import platform


# CLASSES = []
# PROPS = {}

# Declare all modules that this add-on depends on, that may need to be installed. The package and (global) name can be
# set to None, if they are equal to the module name. See import_module and ensure_and_import_module for the explanation
# of the arguments. DO NOT use this to import other parts of your Python add-on, import them as usual with an
# "import" statement.
Dependency = namedtuple("Dependency", ["module", "package", "name", "importable"])
dependencies = (Dependency(module="scipy", package=None, name=None, importable=True),
                Dependency(module="chumpy", package=None, name="ch", importable=True),
                Dependency(module="cv2", package="opencv-python", name=None, importable=True),
                Dependency(module="resampy", package=None, name=None, importable=True),
                Dependency(module="python_speech_features", package=None, name=None, importable=True),
                Dependency(module="tensorflow", package="tensorflow==1.15.2", name="tf", importable=True),
                Dependency(module="sklearn", package="scikit-learn", name=None, importable=True),
                Dependency(module="ipython", package=None, name=None, importable=False),
                Dependency(module="matplotlib", package=None, name=None, importable=True),
                Dependency(module="trimesh", package=None, name=None, importable=True),
                Dependency(module="pyrender", package=None, name=None, importable=False))

dependencies_installed = False

def install_pip():
    try:
        # Check if pip is already installed
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
    except subprocess.CalledProcessError:
        # install pip
        import ensurepip
        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)

    # update pip
    subprocess.run([sys.executable, "-m", "pip", "install",  "-U", "pip"], check=True)


def import_module(module_name, global_name=None, importable="False", reload=True):
    if global_name is None:
        global_name = module_name

    if importable :
        if global_name in globals():
            importlib.reload(globals()[global_name])
            print(module_name + ' module already there')
        else:
            # Attempt to import the module and assign it to globals dictionary. This allow to access the module under
            # the given name, just like the regular import would.
            globals()[global_name] = importlib.import_module(module_name)
            print(module_name + ' module successfully imported')


def install_and_import_module(module_name, package_name=None, global_name=None, importable="False"):
    if package_name is None:
        package_name = module_name
    if global_name is None:
        global_name = module_name

    # Create a copy of the environment variables and modify them for the subprocess call
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"
    # launch pip install
    subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True, env=environ_copy)

    # The installation succeeded, attempt to import the module again
    import_module(module_name, global_name, importable)


# def install_and_import_modules():
#     # Create a copy of the environment variables and modify them for the subprocess call
#     environ_copy = dict(os.environ)
#     environ_copy["PYTHONNOUSERSITE"] = "1"

#     temp_abs_dir = "/Users/sasageyo/Downloads/voca-blender/voca-addon/requirements.txt"
#     subprocess.run([sys.executable, "-m", "pip", "install", "-r", temp_abs_dir], check=True, env=environ_copy)

#     # The installation succeeded, attempt to import the module again
#     for dependency in dependencies:
#         import_module(dependency.module, dependency.name, dependency.importable)

#     # fix protobuf module version
#     subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "protobuf==3.20.0"], check=True, env=environ_copy)

#     # install Mesh from remote wheel
#     temp_whl = "https://github.com/MPI-IS/mesh/releases/download/v0.4/psbody_mesh-0.4-cp37-cp37m-macosx_10_9_x86_64.whl"
#     subprocess.run([sys.executable, "-m", "pip", "install", temp_whl], check=True, env=environ_copy)

#     # fix the OpenGL package
#     src = "/Users/sasageyo/Downloads/voca-blender/script-utils/ctypesloader.py"
#     dst = "/Applications/Blender.app/Contents/Resources/2.92/python/lib/python3.7/site-packages/OpenGL/platform/ctypesloader.py"
#     try:
#         shutil.copy(src, dst)
#         print("File copied successfully.")
#     except shutil.SameFileError:
#         print("Source and destination represents the same file.")
#     except PermissionError:
#         print("Permission denied.")
#     except:
#         print("Error occurred while copying file.")

def complete_installation(): 
    # Create a copy of the environment variables and modify them for the subprocess call
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    # fix protobuf module version
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "protobuf==3.20.0"], check=True, env=environ_copy)

    # install Mesh from remote wheel
    temp_whl = "https://github.com/MPI-IS/mesh/releases/download/v0.4/psbody_mesh-0.4-cp37-cp37m-macosx_10_9_x86_64.whl"
    subprocess.run([sys.executable, "-m", "pip", "install", temp_whl], check=True, env=environ_copy)

    # fix the OpenGL package (ony macOS -> darwin)
    if platform == "darwin":
        # get the path to the patched python file
        src = bpy.utils.user_resource('SCRIPTS', 'addons') + '/voca-addon/utils/ctypesloader.py'
        # get the path to the python library inside the blender app
        dst = sys.path[next(i for i, string in enumerate(sys.path) if 'site-packages' in string)] + "/OpenGL/platform/ctypesloader.py"
        try:
            shutil.copy(src, dst)
            print("OpenGL fixed successfully (macOS only)")
        except shutil.SameFileError:
            print("Source and destination represents the same file.")
        except PermissionError:
            print("Permission denied.")
        except:
            print("Error occurred while copying file.")

# def uninstall_modules():
#     # Create a copy of the environment variables and modify them for the subprocess call
#     environ_copy = dict(os.environ)
#     environ_copy["PYTHONNOUSERSITE"] = "1"

#     temp_abs_dir = "/Users/sasageyo/Downloads/voca-blender/voca-addon/requirements.txt"
#     subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y" "-r", temp_abs_dir], check=True, env=environ_copy)

def uninstall_modules():
    # Create a copy of the environment variables and modify them for the subprocess call
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    for dependency in dependencies:
        # module_to_remove = dependency.package
        # if dependency.package is None:
        #     module_to_remove = dependency.module

        module_to_remove = dependency.module if dependency.package is None else dependency.package

        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", module_to_remove], check=True, env=environ_copy)

# mode = True -> register operators and panels (False is viceversa)
def custom_un_register(mode):
    from . panels import run_model_panel, mesh_import_panel, clear_pannel, edit_mesh_panel
    from . operators import Run_VOCA, Mesh_Import, Mesh_Edit, Mesh_Delete, Mesh_Delete_Other

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

    if mode:
        for PROP in PROPS.values():
            for (prop_name, prop_value) in PROP:
                setattr(bpy.types.Scene, prop_name, prop_value)

        for cls in CLASSES:
            bpy.utils.register_class(cls)
    else:
        for PROP in PROPS.values():
            for (prop_name, prop_value) in PROP:
                delattr(bpy.types.Scene, prop_name)

        for klass in CLASSES:
            bpy.utils.unregister_class(klass)


# GLOBAL Var ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EXAMPLE_PT_warning_panel(bpy.types.Panel):
    bl_label = "Dependencies Warning"
    bl_category = "VOCA"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return not dependencies_installed

    def draw(self, context):
        layout = self.layout

        lines = [f"Please install the missing dependencies for the \"{bl_info.get('name')}\" add-on.",
                 f"1. Open the preferences (Edit > Preferences > Add-ons).",
                 f"2. Search for the \"{bl_info.get('name')}\" add-on.",
                 f"3. Open the details section of the add-on.",
                 f"4. Click on the \"{EXAMPLE_OT_install_dependencies.bl_label}\" button.",
                 f"   This will download and install the missing Python packages, if Blender has the required",
                 f"   permissions."]
    
        for line in lines:
            layout.label(text=line)
            

class EXAMPLE_OT_install_dependencies(bpy.types.Operator):
    bl_idname = "example.install_dependencies"
    bl_label = "Install dependencies"
    bl_description = ("Downloads and installs the required python packages for this add-on. "
                      "Internet connection is required. Blender may have to be started with "
                      "elevated permissions in order to install the package")
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return not dependencies_installed

    def execute(self, context):
        try:
            install_pip()
            # install_and_import_modules()
            for dependency in dependencies:
                install_and_import_module(module_name=dependency.module,
                                          package_name=dependency.package,
                                          global_name=dependency.name,
                                          importable=dependency.importable)

            complete_installation()

        except (subprocess.CalledProcessError, ImportError) as err:
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}

        global dependencies_installed
        dependencies_installed = True

        # Import and register the panels and operators since dependencies are installed
        custom_un_register(True)

        return {"FINISHED"}

class EXAMPLE_OT_uninstall_dependencies(bpy.types.Operator):
    bl_idname = "example.uninstall_dependencies"
    bl_label = "Uninstall dependencies"
    bl_description = ("Uninstalls the required python packages for this add-on. ")
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been uninstalled
        return dependencies_installed

    def execute(self, context):
        try:
            uninstall_modules()
        except (subprocess.CalledProcessError, ImportError) as err:
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}

        global dependencies_installed
        dependencies_installed = False

        # Import and register the panels and operators since dependencies are installed
        custom_un_register(False)

        return {"FINISHED"}

class EXAMPLE_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.operator(EXAMPLE_OT_install_dependencies.bl_idname, icon="CONSOLE")
        layout.operator(EXAMPLE_OT_uninstall_dependencies.bl_idname, icon="CONSOLE")

preference_classes = (EXAMPLE_PT_warning_panel,
                      EXAMPLE_OT_install_dependencies,
                      EXAMPLE_OT_uninstall_dependencies,
                      EXAMPLE_preferences)

# ADD-ON func ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def register():
    global dependencies_installed
    dependencies_installed = False
    
    for cls in preference_classes:
        bpy.utils.register_class(cls)

    try:
        for dependency in dependencies:
            import_module(module_name=dependency.module, global_name=dependency.name, importable=dependency.importable)
        dependencies_installed = True

        # Import and register the panels and operators since dependencies are installed
        custom_un_register(True)
    except ModuleNotFoundError:
        # Don't register other panels, operators etc.
        print("error, some packages are missing")
    
    
def unregister():  
    for cls in preference_classes:
        bpy.utils.unregister_class(cls)
    
    if dependencies_installed:
        custom_un_register(False)

if __name__ == "__main__":
    register()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

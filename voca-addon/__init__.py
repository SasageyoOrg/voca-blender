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
# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #
import bpy
import os
import sys
import subprocess
import importlib
import shutil
from collections import namedtuple
from sys import platform
import time
import platform



# ---------------------------------------------------------------------------- #
#                               Global variables                               #
# ---------------------------------------------------------------------------- #
# Declare all modules that this add-on depends on, that may need to be installed. The package and (global) name can be
# set to None, if they are equal to the module name. See import_module and ensure_and_import_module for the explanation
# of the arguments. DO NOT use this to import other parts of your Python add-on, import them as usual with an
# "import" statement.
Dependency = namedtuple("Dependency", ["module", "package", "name", "importable"])
                
dependencies = (Dependency(module="scipy", package=None, name=None, importable=True),
                Dependency(module="chumpy", package=None, name="ch", importable=True),
                Dependency(module="cv2", package="opencv-python", name=None, importable=True),
                Dependency(module="resampy", package=None, name=None, importable=False),
                Dependency(module="python_speech_features", package=None, name=None, importable=True),
                Dependency(module="tensorflow", package="tensorflow==1.15.2", name="tf", importable=False),
                Dependency(module="sklearn", package="scikit-learn", name=None, importable=True),
                Dependency(module="ipython", package=None, name=None, importable=False),
                Dependency(module="matplotlib", package=None, name=None, importable=True),
                Dependency(module="trimesh", package=None, name=None, importable=True),
                Dependency(module="pyrender", package=None, name=None, importable=False))

dependencies_installed = False
dependency_label = dependencies[0].module
sleep = 1


PROP_DEP = [
    ('installing', bpy.props.BoolProperty(default = False)),
    ('uninstalling', bpy.props.BoolProperty(default = False))
]

# ---------------------------------------------------------------------------- #
#                                   Functions                                  #
# ---------------------------------------------------------------------------- #

# -------------------------------- Refresh all ------------------------------- #

def refresh_all_areas():
    for wm in bpy.data.window_managers:
        for w in wm.windows:
            for area in w.screen.areas:
                area.tag_redraw()



# -------------------------------- Install pip ------------------------------- #
def install_pip():
    time.sleep(sleep)
    # try:
    #     # Check if pip is already installed
    #     subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
    # except subprocess.CalledProcessError:
    # install pip
    import ensurepip
    ensurepip.bootstrap()
    os.environ.pop("PIP_REQ_TRACKER", None)

    # update pip
    subprocess.run([sys.executable, "-m", "pip", "install",  "-U", "pip"], check=True)
    time.sleep(sleep)




# ------------------------------- Import module ------------------------------ #
def import_module(module_name, global_name=None, importable="False", reload=True):
    if global_name is None:
        global_name = module_name

    if importable :
        print(f'importing {module_name}')
        if(module_name == 'numba'):
            os.environ['NUMBA_DISABLE_INTEL_SVML'] = '1'
        if global_name in globals():
            importlib.reload(globals()[global_name])
            print(module_name + ' module already there')
        else:
            # Attempt to import the module and assign it to globals dictionary. This allow to access the module under
            # the given name, just like the regular import would.
            globals()[global_name] = importlib.import_module(module_name)
            print(module_name + ' module successfully imported')




# ------------------------- Install and import module ------------------------ #
def install_and_import_module(module_name, package_name=None, global_name=None, importable="False"):
    time.sleep(sleep)
    global dependency_label
    dependency_label = module_name
    if package_name is None:
        package_name = module_name
    if global_name is None:
        global_name = module_name

    # Create a copy of the environment variables and modify them for the subprocess call
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"
    # launch pip install
    print('--- Installing module: '+ module_name + ' ---')
    subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True, env=environ_copy)

    # The installation succeeded, attempt to import the module again

    
    import_module(module_name, global_name, importable)
    time.sleep(sleep)



# --------------------------- Complete installation -------------------------- #
def complete_installation(): 
    time.sleep(sleep)
    # Create a copy of the environment variables and modify them for the subprocess call
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    # fix protobuf module version
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "protobuf==3.20.0"], check=True, env=environ_copy)

    # install Mesh from remote wheel
    if platform == "darwin":
        # OS X
        temp_whl = "https://github.com/MPI-IS/mesh/releases/download/v0.4/psbody_mesh-0.4-cp37-cp37m-macosx_10_9_x86_64.whl"
    else:
        # linux
        temp_whl = "https://github.com/MPI-IS/mesh/releases/download/v0.4/psbody_mesh-0.4-cp37-cp37m-linux_x86_64.whl"

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
    time.sleep(sleep)




# ----------------------------- Uninstall modules ---------------------------- #
def uninstall_modules():
    # Create a copy of the environment variables and modify them for the subprocess call
    environ_copy = dict(os.environ)
    environ_copy["PYTHONNOUSERSITE"] = "1"

    for dependency in dependencies:
        module_to_remove = dependency.module if dependency.package is None else dependency.package

        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", module_to_remove], check=True, env=environ_copy)

# mode = True -> register operators and panels (False is viceversa)
def custom_un_register(mode):
    from . panels import run_model_panel, mesh_import_panel, dev_pannel
    from . operators import Run_VOCA, Mesh_Import, Mesh_Edit, Mesh_Delete, Mesh_Delete_Other

    CLASSES = [
        Run_VOCA,
        Mesh_Import,
        Mesh_Edit,
        run_model_panel,
        mesh_import_panel,
        dev_pannel,
        Mesh_Delete,
        Mesh_Delete_Other
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



Operations = {
    "Installing pip...": install_pip,
    "Installing scipy...": install_and_import_module,
    "Installing chumpy...": install_and_import_module,
    "Installing cv2...": install_and_import_module,
    "Installing resampy...": install_and_import_module,
    "Installing python_speech_features...": install_and_import_module,
    "Installing tensorflow...": install_and_import_module,
    "Installing sklearn...": install_and_import_module,
    "Installing ipython...": install_and_import_module,
    "Installing matplotlib...": install_and_import_module,
    "Installing trimesh...": install_and_import_module,
    "Installing pyrender...": install_and_import_module,
    "Completing installation..": complete_installation
}
# ---------------------------------------------------------------------------- #
#                                    Panels                                    #
# ---------------------------------------------------------------------------- #
# ------------------------------- Warning Panel ------------------------------ #
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
        obj = context.object
        
        if not context.scene.installing :
            lines = [f"Please install the missing dependencies for the \"{bl_info.get('name')}\" add-on.",
                    f"1. Open the preferences (Edit > Preferences > Add-ons).",
                    f"2. Search for the \"{bl_info.get('name')}\" add-on.",
                    f"3. Open the details section of the add-on.",
                    f"4. Click on the \"{EXAMPLE_OT_install_dependencies.bl_label}\" button.",
                    f"   This will download and install the missing Python packages, if Blender has the required",
                    f"   permissions."]
        else :
            lines = [f"Installing the addon's dependencies",
                    f"Please, wait until the end of the process."]
            

        for line in lines:
            layout.label(text=line)
            
            
            
# ---------------------------------------------------------------------------- #
#                                   Operators                                  #
# ---------------------------------------------------------------------------- #



# ----------------------- Install dependencies operator ---------------------- #

class EXAMPLE_OT_install_dependencies(bpy.types.Operator):
    bl_idname = "example.install_dependencies"
    bl_label = "Install dependencies"
    bl_description = ("Downloads and installs the required python packages for this add-on. "
                      "Internet connection is required. Blender may have to be started with "
                      "elevated permissions in order to install the package")
    bl_options = {"REGISTER", "INTERNAL"}
    
    def __init__(self):

        self.step = 0
        self.timer = None
        self.done = False
        self.max_step = None

        # timer count, need to let a little bit of space between updates otherwise gui will not have time to update
        self.timer_count = 0

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return not dependencies_installed


    def modal(self, context, event):
        

        global Operations
        global dependency_label
        global dependencies_installed
        #update progress bar
        if not self.done:
            print(f"Updating: {self.step+1}/{self.max_step}")
            #update progess bar
            context.object.progress = ((self.step+1)/(self.max_step))*100
            #update label
            progress_label = list(Operations.keys())[self.step]
            context.object.progress_label = progress_label

            #send update signal
            context.area.tag_redraw()

        #by running a timer at the same time of our modal operator
        #we are guaranteed that update is done correctly in the interface

        if event.type == 'TIMER':

            #but wee need a little time off between timers to ensure that blender have time to breath, so we have updated inteface
            self.timer_count += 1
            if self.timer_count == 10:
                self.timer_count = 0

                if self.done:

                    print("Finished")

                    self.step = 0
                    context.object.progress = 0
                    context.window_manager.event_timer_remove(self.timer)
                    context.area.tag_redraw()
                    dependencies_installed = True
                    custom_un_register(True)
                    return {'FINISHED'}
            
                # RUNNING INSTALL OPERATIONS
                if self.step < self.max_step:
                    print(self.step)
                    try:
                        if(self.step >= 1 and (self.step-1 < len(dependencies))):
                            list(Operations.values())[self.step](module_name=dependencies[self.step - 1].module,
                                                                    package_name=dependencies[self.step - 1].package,
                                                                    global_name=dependencies[self.step - 1].name,
                                                                    importable=dependencies[self.step - 1].importable)
                        else:
                            list(Operations.values())[self.step]()
                            
                        #run step function

                        self.step += 1
                        if self.step == self.max_step:
                            self.done = True
                    except (subprocess.CalledProcessError, ImportError) as err:
                        self.report({"ERROR"}, str(err))
                        print("Finished")
                        self.step = 0
                        context.object.progress = 0
                        context.window_manager.event_timer_remove(self.timer)
                        context.area.tag_redraw()

                        return {'FINISHED'}
                    return {'RUNNING_MODAL'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):

        print("")
        print("Invoke")

        #terermine max stepa
        global Operations
        if self.max_step == None:
            self.max_step = len(Operations.keys())

        context.window_manager.modal_handler_add(self)

        #run timer
        self.timer = context.window_manager.event_timer_add(
            0.1, window=context.window)

        return {'RUNNING_MODAL'}

   
   
   
# ---------------------- Uninstall dependencies operator --------------------- #
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
    
    
# ----------------------------- Addon prferences ----------------------------- #
class EXAMPLE_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    def draw(self, context):
        obj = context.object
        layout = self.layout
        if obj.progress:
            progress_bar = layout.row()
            progress_bar.prop(bpy.context.object, "progress")
            progress_lbl = layout.row()
            progress_lbl.active = False
            progress_lbl.label(text=bpy.context.object.progress_label)
        else:
            row = layout.row()
            row.operator(EXAMPLE_OT_install_dependencies.bl_idname, icon="CONSOLE")
            row.operator(EXAMPLE_OT_uninstall_dependencies.bl_idname, icon="CONSOLE")


preference_classes = (EXAMPLE_PT_warning_panel,
                    EXAMPLE_OT_install_dependencies,
                    EXAMPLE_OT_uninstall_dependencies,
                    EXAMPLE_preferences)

# ---------------------------------------------------------------------------- #
#                             Register / Unregister                            #
# ---------------------------------------------------------------------------- #
def register():
    
    # custom_un_register(False)
    global dependencies_installed
    dependencies_installed = False
    print('Registering classes...')
    for cls in preference_classes:
        print(f'Registering class: {cls}')
        bpy.utils.register_class(cls)
    print('Initializing props...')
    for (prop_name, prop_value) in PROP_DEP:
        setattr(bpy.types.Scene, prop_name, prop_value)
        print(f'{prop_name}: {prop_value}')


    bpy.types.Object.progress = bpy.props.FloatProperty(
        name="Progress", subtype="PERCENTAGE", soft_min=0, soft_max=100, precision=0,)
    bpy.types.Object.progress_label = bpy.props.StringProperty()

    try:
        for dependency in dependencies:
            import_module(module_name=dependency.module, global_name=dependency.name, importable=dependency.importable)
        dependencies_installed = True

        # Import and register the panels and operators since dependencies are installed
        custom_un_register(True)
    except Exception as e :
        # Don't register other panels, operators etc.
        print(f"Exception occured: {e}")
    
def unregister():  
    for cls in preference_classes:
        bpy.utils.unregister_class(cls)
    for (prop_name, prop_value) in PROP_DEP:
        delattr(bpy.types.Scene, prop_name)
    
    if dependencies_installed:
        custom_un_register(False)

if __name__ == "__main__":
    register()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

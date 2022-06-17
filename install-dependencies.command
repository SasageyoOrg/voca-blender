#!/bin/sh

bold=$(tput bold)
normal=$(tput sgr0)

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
SCRIPT_PATH="$SCRIPT_DIR/script-utils/ctypesloader.py"

# go to home directory
cd $HOME

# update brew (install if needed)
echo "${bold}> checking homebrew installation...${normal}"
which -s brew
if [[ $? != 0 ]] ; then
    # Install Homebrew
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo "  ${bold}homebrew installed${normal}"
else
    brew update -q
    echo "  ${bold}ok${normal}"
fi

# install pyenv
echo "\n${bold}> installing brew packages (git, wget, pyenv)...${normal}"
if brew install git wget pyenv ; then
    echo "  ${bold}ok${normal}"
else
    echo "  ${bold}failed${normal}"
    exit 1
fi

# install python 3.7.13 if not present and set it as default
echo "\n${bold}> installing python version 3.7.13 (required by voca)${normal}"
if ! grep -q 'eval "$(pyenv init -)"' '.zshrc' ; then
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc
    . $HOME/.zshrc
fi

if
    pyenv install 3.7.13 -s &&
    pyenv local 3.7.13 &&
    . $HOME/.zshrc
then
    echo "  ${bold}ok${normal}"
else
    echo "  ${bold}failed${normal}"
    exit 1
fi

BLENDER_SCRIPTS_DIR="/Applications/Blender.app/Contents/Resources/2.92/scripts"
BLENDER_MODULE_DIR="/Applications/Blender.app/Contents/Resources/2.92/scripts/modules"

# create the 'modules' directory in blender if not already there
mkdir -p "$BLENDER_SCRIPTS_DIR"/modules
# make sure pip version is up-to-date
pip install -t $BLENDER_MODULE_DIR -U pip
# install dependencies
echo "\n${bold}> installing pip modules...${normal}"
pip install -t $BLENDER_MODULE_DIR wget numpy scipy chumpy opencv-python resampy python-speech-features tensorflow==1.15.2 scikit-learn image ipython matplotlib trimesh pyrender
pip install -t $BLENDER_MODULE_DIR  --upgrade protobuf==3.20.0
pip install -t $BLENDER_MODULE_DIR https://github.com/MPI-IS/mesh/releases/download/v0.4/psbody_mesh-0.4-cp37-cp37m-macosx_10_9_x86_64.whl
cp $SCRIPT_PATH /Applications/Blender.app/Contents/Resources/2.92/scripts/modules/OpenGL/platform/ctypesloader.py
echo "  ${bold}ok${normal}"

# reset the python system version
pyenv local system
. $HOME/.zshrc

echo "\n${bold}> blender voca addon dependencies installed successfully!${normal}"
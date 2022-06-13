#!/bin/sh

bold=$(tput bold)
normal=$(tput sgr0)

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
SCRIPT_PATH="$SCRIPT_DIR/script-utils/ctypesloader.py"

# go to home directory
cd ~

# update brew (install if needed)
echo "${bold}> checking homebrew installation...${normal}"
which -s brew
if [[ $? != 0 ]] ; then
    # Install Homebrew
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
    brew update -q
fi
echo "  ok"

# install pyenv
echo "\n${bold}> installing brew packages...${normal}"
brew install pyenv wget
echo "  ok"

# install python 3.7.13 if not present and set it as default
echo "\n${bold}> installing python version 3.7.13 (required by voca)${normal}"
pyenv install 3.7.13 -s
pyenv local 3.7.13
if ! grep -q 'eval "$(pyenv init -)"' '.zshrc' ; then
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc
    #exec "$SHELL"
    . ~/.zshrc
fi
echo "  ok"

# create a hidden directory for the venv in the home
echo "\n${bold}> creating the python virtual environment${normal}"
mkdir -p .virtualenvs
# create the virtual environment and activate it
python3 -m venv .virtualenvs/vocablender
source .virtualenvs/vocablender/bin/activate
# make sure pip version is up-to-date
pip install -U pip
echo "  ok"
# install dependencies
echo "\n${bold}> installing pip modules...${normal}"
pip install wget numpy scipy chumpy opencv-python resampy python-speech-features tensorflow==1.15.2 scikit-learn image ipython matplotlib trimesh pyrender
pip install --upgrade protobuf==3.20.0
cp $SCRIPT_PATH .virtualenvs/vocablender/lib/python3.7/site-packages/OpenGL/platform/ctypesloader.py
echo "  ok"

# install mesh lib
echo "\n${bold}> installing psbody-mesh...${normal}"
pip install https://github.com/MPI-IS/mesh/releases/download/v0.4/psbody_mesh-0.4-cp37-cp37m-macosx_10_9_x86_64.whl
echo "  ok"

# reset the python system version
pyenv local system
. ~/.zshrc

echo "\n${bold}> blender voca addon dependencies installed successfully!${normal}"

# install mesh lib
#brew install boost
# clone the repository
#git clone https://github.com/MPI-IS/mesh.git .virtualenvs
#  compile and install the psbody-mesh package using the makefile 
#BOOSTPATH=$(brew --prefix boost)
#BOOST_INCLUDE_DIRS=$BOOSTPATH make all
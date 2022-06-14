#!/bin/bash

bold=$(tput bold)
normal=$(tput sgr0)

shopt -s xpg_echo

# go to home directory
cd $HOME

# install pyenv
echo "${bold}> installing pyenv...${normal}"
if ! command -v pyenv &> /dev/null
then
    sudo apt-get update
    sudo apt-get install make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \ 
    git ffmpeg
    if curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash ; then
        #echo "  ${bold}pyenv installed! please, run this script again to continue${normal}"
        #exec bash
        . $HOME/.bashrc
        echo "  ${bold}ok${normal}"
    else
        echo "  ${bold}failed${normal}"
        exit 1
    fi
else
    echo "  ${bold}skip${normal}"
fi


# install python 3.7.13 if not present and set it as default
echo "\n${bold}> installing python version 3.7.13 (required by voca)${normal}"
if ! grep -q 'eval "$(pyenv init -)"' '.bashrc' ; then
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    . $HOME/.bashrc
fi

if
    pyenv install 3.7.13 -s &&
    pyenv local 3.7.13 &&
    . $HOME/.bashrc
then
    echo "  ${bold}ok${normal}"
else
    echo "  ${bold}failed${normal}"
    exit 1
fi

# create a hidden directory for the venv in the home
echo "\n${bold}> creating the python virtual environment${normal}"
mkdir -p .virtualenvs
# create the virtual environment and activate it
python3 -m venv .virtualenvs/vocablender
source .virtualenvs/vocablender/bin/activate
# make sure pip version is up-to-date
pip install -U pip
echo "  ${bold}ok${normal}"
# install dependencies
echo "\n${bold}> installing pip modules...${normal}"
pip install wget numpy scipy chumpy opencv-python resampy python-speech-features tensorflow==1.15.2 scikit-learn image ipython matplotlib trimesh pyrender
pip install --upgrade protobuf==3.20.0
echo "  ${bold}ok${normal}"

# install mesh lib
echo "\n${bold}> installing psbody-mesh...${normal}"
pip install https://github.com/MPI-IS/mesh/releases/download/v0.4/psbody_mesh-0.4-cp37-cp37m-linux_x86_64.whl
echo "  ${bold}ok${normal}"

# reset the python system version
pyenv local system
. $HOME/.bashrc

echo "\n${bold}> blender voca addon dependencies installed successfully!${normal}"
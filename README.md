<p align="center">
  <a href="" rel="noopener">
  <img style=vertical-align:middle; height=100 src="imgs\voca.png " alt="Voca logo"></a>
  <img style=vertical-align:middle; height=150px src="https://download.blender.org/branding/community/blender_community_badge_white.png" alt="Blender logo"></a>
</p>

<h1 align="center">VOCA Blender Addon</br><sub></sub></h1>

# 📝 Table of Contents
- [About](#about)
- [Project Topology](#project-topology)
- [Installation and usage](#ins-usage)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

# 📋About <a name = "about"></a>
<p align="center" >
  <img height=200px src="imgs\speech_driven_animation.gif" alt="Voca gif"></a>
</p>
VOCA is a simple and generic speech-driven facial animation framework that works across a range of identities. This add-on integrates VOCA withing Blender and allows the user to:
 * Run VOCA and synthesize a character animation given an speech signal. VOCA outputs a set meshes with .obj extension which must to be imported.
 * Import the output meshes of VOCA and generate from them a single animated mesh.

For more details please see the scientific publication of the VOCA framework [here](https://voca.is.tue.mpg.de/).

The original VOCA framework repository can be found here [here](https://github.com/TimoBolkart/voca).




# 👩‍💻Installation and usage <a name="ins-usage"></a>
1. The add-on works with Python 3.7 and requires some dependencies that can be installed by running the dedicated shell script.
  * On MacOS run `.\install-dependencies.command`
  * On Linux run `.\install-dependencies.sh`
  
    The script will download Python 3.7 if not present, will create a dedicated virtual envoirment and install the dependencies within it.


2. Download the latest release.
3. Import the downloaded .zip archive in Blender (Edit > Preferences > Add-ons > Install) and enable the add-on.
4. The add-on options are accessible in the 3D View side panel.

<p align="center">
  <img height=350px src="imgs\side_panel.png" alt="Project logo"></a>
</p>

## To generate a new sequence of meshes:
1. Expand the 'Run VOCA Model' panel.
2. Select the right path for the mesh template (.ply) to animate, the audio file with the speech signal and the desired output directory.
3. Hit 'Run' and wait the end of the process.

## To import the VOCA-generated meshes and generate the animated mesh:
1. Expand the 'Import Mesh' panel.
2. Select the path to the audio file and the output directory.
3. Hit 'Import' and wait.

## The 'Clear Meshes Panels' allows you to:
  * Hide/unhide non-VOCA meshes.
  * Remove all meshes from the scene.
  * Remove all non-VOCA meshes from the scene.

# 🗂 Project Topology <a name="project-topology"></a>


```
voca-blender
├─ imgs
│  ├─ Logo_Blender.svg.png
│  ├─ side_panel.png
│  ├─ speech_driven_animation.gif
│  └─ voca.png
├─ install-dependencies.command
├─ install-dependencies.sh
├─ LICENSE
├─ README.md
├─ script-utils
│  └─ ctypesloader.py
└─ voca-addon
   ├─ audio
   │  ├─ sentence20.wav
   │  └─ test_sentence.wav
   ├─ flame
   │  └─ generic_model.pkl
   ├─ model
   ├─ operators.py
   ├─ panels.py
   ├─ smpl_webuser
   │  ├─ lbs.py
   │  ├─ LICENSE.txt
   │  ├─ posemapper.py
   │  ├─ serialization.py
   │  ├─ verts.py
   │  └─ __init__.py
   ├─ template
   │  └─ FLAME_sample.ply
   ├─ utils
   │  ├─ audio_handler.py
   │  ├─ edit_sequences.py
   │  └─ inference.py
   └─ __init__.py

```
# ✍️ Authors <a name = "authors"></a>

- Conti Edoardo [@edoardo-conti](https://github.com/edoardo-conti)
- Federici Lorenzo [@lorenzo-federici](https://github.com/lorenzo-federici)
- Melnic Andrian [@andrian-melnic](https://github.com/andrian-melnic)

# 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Computer Graphics e Multimedia Class - Professor <a href="https://vrai.dii.univpm.it/primo.zingaretti"><i>Primo Zingaretti</i></a>


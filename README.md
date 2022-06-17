<p align="center">
  <a href="" rel="noopener">
  <img style=vertical-align:middle; height=150px src="resources/blender_community_badge_white.png" alt="Blender logo"></a>
</p>

<h1 align="center">VOCA Blender Addon</br><sub></sub></h1>

# 📝 Table of Contents
- [About](#about)
- [Project Topology](#project-topology)
- [Installation and Usage](#ins-usage)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

# 📋About <a name = "about"></a>
<p align="center" >
  <img width=80% src="resources\voca_blender_animation.gif" alt="Voca gif"></a>
</p>
VOCA is a simple and generic speech-driven facial animation framework that works across a range of identities. This add-on integrates VOCA withing Blender and allows the user to:

 * Run VOCA and synthesize a character animation given an speech signal. VOCA outputs a set meshes with .obj extension which must to be imported.
 * Import the output meshes of VOCA and generate from them a single animated mesh.

For more details please see the scientific publication of the VOCA framework [here](https://voca.is.tue.mpg.de/).

The original VOCA framework repository can be found here [here](https://github.com/TimoBolkart/voca).

# 👩‍💻Installation and Usage <a name="ins-usage"></a>
1. The add-on works with \Blender v2.92.0 (python 3.7) and requires some dependencies that can be installed directly from the preferences panel.
2. Download the latest release.
3. Import the downloaded .zip archive in Blender (Edit > Preferences > Add-ons > Install) and enable the add-on.
4. Install the dependencies by clicking the dedicated button
5. The add-on options are accessible in the 3D View side panel named "VOCA"
6. (optional) If you want to uninstall the addon, you can also uninstall the dependencies from the preferences panel.
<p align="center" >
  <img style=vertical-align:middle; width=42% src="resources\install.png"></a>
  <img style=vertical-align:middle; width=40.9% src="resources\uninstall.png"></a>
</p>
<p align="center" >
<img width=48% src="resources\panel_warning.png"></a>
</p>

## To generate a new sequence of meshes:
1. Expand the 'Run VOCA Model' panel.
2. Select the right path for the mesh template (.ply) to animate, the audio file with the speech signal and the desired output directory.
3. Hit 'Run' and wait the end of the process.
<p align="center" >
  <img src="resources\panel_run.png"></a>
</p>

## To import the VOCA-generated meshes and generate the animated mesh:
1. Expand the 'Import Mesh' panel.
2. Select the path to the audio file and the output directory.
3. Hit 'Import' and wait.
<p align="center" >
  <img src="resources\panel_import.png"></a>
</p>

## The 'Dev' panel allows you to:
  * Hide/unhide non-VOCA meshes.
  * Remove all meshes from the scene.
  * Remove all non-VOCA meshes from the scene.
  * Edit sequences (flame parameters: head, pose, blink)
<p align="center" >
  <img src="resources\panel_dev.png"></a>
</p>

# 🗂 Project Topology <a name="project-topology"></a>
```
voca-blender/
├─ voca-addon/
│  ├─ audio/
│  │  ├─ sentence20.wav
│  │  └─ test_sentence.wav
│  ├─ flame/
│  │  └─ generic_model.pkl
│  ├─ model/
│  │  └─ gstep.model.*
│  ├─ smpl_webuser/
│  │  ├─ lbs.py
│  │  ├─ posemapper.py
│  │  ├─ serialization.py
│  │  └─ verts.py
│  ├─ template/
│  │  └─ FLAME_sample.ply
│  ├─ utils/
│  |  ├─ ctypesloader.py
│  │  ├─ audio_handler.py
│  │  ├─ edit_sequences.py
│  │  └─ inference.py
│  ├─ operators.py
│  ├─ panels.py
│  └─ __init__.py
├─ install-dependencies.command
├─ install-dependencies.sh
├─ LICENSE
└─ README.md
```

# ✍️ Authors <a name = "authors"></a>
- Conti Edoardo [@edoardo-conti](https://github.com/edoardo-conti)
- Federici Lorenzo [@lorenzo-federici](https://github.com/lorenzo-federici)
- Melnic Andrian [@andrian-melnic](https://github.com/andrian-melnic)

# 🎉 Acknowledgements <a name = "acknowledgement"></a>
- Computer Graphics e Multimedia Class - Professor <a href="https://vrai.dii.univpm.it/primo.zingaretti"><i>Primo Zingaretti</i></a>

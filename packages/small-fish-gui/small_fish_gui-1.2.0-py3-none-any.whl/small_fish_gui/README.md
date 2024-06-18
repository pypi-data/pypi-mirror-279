# Small Fish
**Small Fish** is a python application for the analysis of smFish images. It provides a ready to use graphical interface to combine famous python packages for cell analysis without any need for coding.

Cell segmentation (**2D**) is peformed using *cellpose* (published work) : https://github.com/MouseLand/cellpose; compatible with your own cellpose models.

Spot detection is performed via *big-fish* (published work) : https://github.com/fish-quant/big-fish

Time stacks are not yet supported.

## What can you do with small fish ?

- Single molecule quantification (including a lot of spatial features)
- Foci/Transcription site quantification
- Nuclear signal quantification
- Signal to noise analysis
- multichannel colocalisation

## Installation

It is higly recommanded to create a specific [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) or [virtual](https://docs.python.org/3.6/library/venv.html) environnement to install small fish.

```bash
conda create -n small_fish python=3.8
conda activate small_fish
```
Then download the small_fish package : 
```bash
pip install small_fish_gui
```
<b> (Recommended) </b> Results visualisation is achieved through *Napari* which you can install with :

```bash
pip install napari[all]
```

## Run Small fish

First activate your python environnement : 
```bash
activate small_fish
```
Then launch Small fish : 
```bash
python -m small_fish_gui
```

## Cellpose configuration

If you want to train your own cellpose model or set-up your GPU you can follow the official cellpose documentation, just remember to **first activate your small_fish environnement**.

## Developpement

Optional features to include in future versions : 
- batch processing
- time stack (which would include cell tracking)
- 3D segmentation

# 3D ECM Method for Describing Three Dimensional Layering

This repository holds a working version of scripts and data for calculation of 3D Layer Orientations on 60 m of ALHIC2201 and ALHIC2302

## Contents
- data/
  - ALHIC2302/ - _3D ECM Data from ALHIC2302 Core_
  - ALHIC2201/ - _3D ECM Data from ALHIC2201 Core_
  - angles/ - _data containing dip angle calculations, used to transfer between scripts_
  - metadata.csv - _csv file containing metadata for all data files. This is helpful when reading in data (used in scripts)_
- scripts/
  - basic plots/ - simple figures for ALHIC2302 and ALHIC2201
    - alhic2201_initialplots.py - plot AC and DC ECM data from ALHIC2201
    - alhic2302_initialplots.py - plot AC and DC ECM data from ALHIC2302
    - alhic2201_initialplots.py - plot ECM data from one section for use in paper.
- core_scripts/ - basic scripts used in others. Includes definition of ECM class
  - layer_orientations - scripts to determine 3D layer orientation and plot results
  - threedim_plotting - three dimensional plots (as seen in paper)
- radar/
  - explore_picks.ipynb - script to load radar data and make relevant figures
- threedim_plotting/
  - alhic23_paper_3Dplot.py - make 3D plot for paper
- layer_orientations
  - get_truedip.py - convert aparent dip calcs to true dip
  - master_orientation - calculate aparent dip on each page
  - orientation_plots_vectormethod.ipynb - make plots showing dip and dip direction
  - paper_orientationplot.py - make plot showing aparent dip calculation method (for paper

- README.md - this file, describes contents and use

## Use
The scripts in this repository are all written in python. Many are jupyter notebooks. The packages needed in the conda environment are included in the environment_3d-ecm.yml file.

# 3D ECM Method for Describing Three Dimensional Layering

This repository holds a working version of scripts and data for calculation of 3D Layer Orientations on 60 m of ALHIC2201 and ALHIC2302

## Contents
- data/
  - ALHIC2302/ - _3D ECM Data from ALHIC2302 Core_
  - ALHIC2201/ - _3D ECM Data from ALHIC2201 Core_
  - metadata.csv - _csv file containing metadata for all data files. This is helpful when reading in data (used in scripts)_
- scripts/
  - basic plots/ - simple figures for ALHIC2302 and ALHIC2201
    - alhic2201_initialplots.py - plot AC and DC ECM data from ALHIC2201
    - alhic2302_initialplots.py - plot AC and DC ECM data from ALHIC2302
  - core_scripts/ - basic scripts used in others. Includes definition of ECM class
    - 
  - layer_orientations - scripts to determine 3D layer orientation and plot results
  - threedim_plotting - three dimensional plots (as seen in paper)
- README.md - this file, describes contents and use

## Use
The scripts in this repository are all written in python. The packages needed in the conda environment are included in the environment_3d-ecm.yml file.

[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/calekochenour/remote-sensing-textbook/master)
[![Launch Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calekochenour/remote-sensing-textbook/blob/master/notebooks)
[![BSD 3-Clause License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

# Remote Sensing with Google Earth Engine

This [remote sensing textbook](https://calekochenour.github.io/remote-sensing-textbook/) provides text and examples for how to use Google Earth Engine to work through the remote sensing data workflow:

* Acquisition and Preprocessing;
* Processing;
* Postprocessing;
* Visualization; and,
* Export.

The [remote sensing textbook](https://calekochenour.github.io/remote-sensing-textbook/) includes code in `JavaScript` and `Python` for creating remote sensing analyses and workflows.

## Contents

The project contains folders for the textbook content as well as other files necessary to re-create the book locally.

### `content/`

Contains source files for the textbook content (both pre-build and post-build).

### `notebooks/`

Contains Jupyter Notebooks for the Python code in the textbook (independent of the textbook build).

### `Makefile`

Contains instructions to automate Jupyter Book builds and GitHub commits.

### `environment.yml`

Contains all information to create the Conda environment required to run the Jupyter Notebook files in the `notebooks/` folder.  

# Remote Sensing with Google Earth Engine

This [remote sensing textbook](https://calekochenour.github.io/remote-sensing-textbook/) provides text and examples for how to use Google Earth Engine to work through the remote sensing data workflow:

* Acquisition and Pre-Processing;
* Processing;
* Post-Processing;
* Visualization; and,
* Export.

The [remote sensing textbook](https://calekochenour.github.io/remote-sensing-textbook/) includes code in `JavaScript` and `Python` for creating remote sensing analyses and workflows.

## Contents

The project contains folders for the textbook content as well as other files necessary to re-create the book locally.

### `content/`

Contains source files for the textbook content (both pre-build and post-build).

### `notebooks/`

Contains Jupyter Notebooks for the Python code in the textbook (independent of the textbook build).

Run Jupyter Notebooks in Google Colab:

[![image](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/calekochenour/remote-sensing-textbook/blob/master/notebooks)

### `environment.yml`

Contains all information to create the Conda environment required to:

* Build the textbook from source files in the `contents/` folder; and,
* Run the Jupyter Notebook files in the `notebooks/` folder.  

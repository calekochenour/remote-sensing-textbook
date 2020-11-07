# Image Composites

## Environment Setup

```{code-block} python
def initialize_earth_engine():
    """Initializes the Earth Engine Python API.

    Returns
    -------
    str

    Example
    -------
        >>> import ee
        >>> initialize_earth_engine()
        Imported ee. Initialized Earth Engine Python API.
    """
    # Import ee if not already imported
    import sys
    if "ee" not in sys.modules:
        import ee
        global ee

    # Initialize Earth Engine Python API
    try:
        ee.Initialize()
    except Exception:
        ee.Authenticate()
        ee.Initialize()

    return print("Imported ee. Initialized Earth Engine Python API.")
```

```{code-block} python
def import_geemap():
    """Imports the geemap package (environment-dependent, Google Colab
    vs. Jupyter/Binder).

    Returns
    -------
    environment : str
        Message indicating the geemap has been imported into the
        environment. The message differs based on the environment.

    Example
    -------
        >>> import_geemap()
        Notebook running in Jupyter/Binder. Imported geemap as gm.
    """
    # Check for Google Colab
    try:
        import google.colab
    # Notebook running in Jupyter/Binder
    except ImportError:
        running_in_colab = False
    # Notebook running in Google Colab
    else:
        running_in_colab = True

    # Import geemap based on environment (Google Colab vs. Jupyter/Binder)
    if running_in_colab:
        import subprocess
        subprocess.check_call(["python", "-m", "pip", "install", "geemap"])
        import geemap.eefolium as gm
        global gm
        environment = print(
            "Notebook running in Google Colab. Imported geemap.folium as gm."
        )
    else:
        import geemap as gm
        global gm
        environment = print(
            "Notebook running in Jupyter/Binder. Imported geemap as gm."
        )

    return environment
```

```{code-block} python
# Initialize Earth Engine Python API
initialize_earth_engine()

# Import geemap
import_geemap()
```

```{code-block} python
def add_ndvi(image):
    """Calculates and adds the NDVI band to a Landsat 8 image.

    Parameters
    ----------
    image : ee.image.Image object
        Landsat 8 image.

    Returns
    -------
    image_ndvi : ee.image.Image object
        Input landsat 8 image with the NDVI band added, named 'NDVI'.

    Example
    -------
        >>>
        >>>
        >>>
        >>>
    """
    # Calculate and add NDVI band
    image_ndvi = image.addBands(
        image.normalizedDifference(["B5", "B4"]).rename("NDVI")
    )

    return image_ndvi
```

## Data Acquisition & Pre-Processing
```{code-block} python
#  No data acquisition and preprocessing in the lab.
```

## Data Processing
```{code-block} python
# No data processing in this lab.
```

## Data Visualization
```{code-block} python
# No data visualization in this lab.
```

## Data Postprocessing
```{code-block} python
# No data postprocessing in this lab.
```

## Data Export
```{code-block} python
# No data export in this lab.
```

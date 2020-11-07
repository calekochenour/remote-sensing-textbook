# Qualitative Change Detection

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
    except Exception as error:
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
    except ImportError as error:
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

## Data Acquisition & Preprocessing

```{code-block} python
# Get boundary for Rocky Mountain National Park, Colorado
rmnp_boundary = ee.FeatureCollection(
    "users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon"
)

# Get Landsat 8 collection
landsat8_t1_sr = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")

# Filter Landsat 8 Tier 1 SR to snow-on conditions near RMNP, 2018
co_snow_on_2018 = (
    landsat8_t1_sr.filterDate("2018-03-01", "2018-04-30")
    .filterBounds(rmnp_boundary)
    .sort("CLOUD_COVER")
    .first()
)

# Filter Landsat 8 Tier 1 SR to snow-off conditions near RMNP, 2018
co_snow_off_2018 = (
    landsat8_t1_sr.filterDate("2018-07-01", "2018-08-31")
    .filterBounds(rmnp_boundary)
    .sort("CLOUD_COVER")
    .first()
)

# Clip snow-on and snow-off imagery to RMNP boundary
rmnp_snow_on_2018 = co_snow_on_2018.clip(rmnp_boundary)
rmnp_snow_off_2018 = co_snow_off_2018.clip(rmnp_boundary)
```

## Data Processing
```{code-block} python
# No data processing in this lab.
```

## Data Postprocessing
```
# No data postprocessing in this lab.
```

## Data Visualization
```{code-block} python
# Create interactive map for visualization and set options
if "rmnp_map" in globals():
    del rmnp_map
    rmnp_map = gm.Map()
    rmnp_map.setOptions("SATELLITE")
    rmnp_map.setCenter(lon=-105.6836, lat=40.3428, zoom=10)
else:
    rmnp_map = gm.Map()
    rmnp_map.setOptions("SATELLITE")
    rmnp_map.setCenter(lon=-105.6836, lat=40.3428, zoom=10)
```

```{code-block} python
# Define Landsat visualization parameters
l8_vis_params_rgb = {"bands": ["B4", "B3", "B2"], "min": 0, "max": 3000}
l8_vis_params_cir = {"bands": ["B5", "B4", "B3"], "min": 0, "max": 3000}

# Define RMNP boundary visualization parameters
rmnp_boundary_vis = (
    ee.Image()
    .byte()
    .paint(**{"featureCollection": rmnp_boundary, "color": 1, "width": 3})
)

# Add snow-on and snow-off images to map, RGB and CIR
rmnp_map.addLayer(
    rmnp_snow_on_2018,
    l8_vis_params_rgb,
    "Landsat 8 - RGB - 2018 - RMNP - Snow On",
)

rmnp_map.addLayer(
    rmnp_snow_on_2018,
    l8_vis_params_cir,
    "Landsat 8 - CIR - 2018 - RMNP - Snow On",
)

rmnp_map.addLayer(
    rmnp_snow_off_2018,
    l8_vis_params_rgb,
    "Landsat 8 - RGB - 2018 - RMNP - Snow Off",
)

rmnp_map.addLayer(
    rmnp_snow_off_2018,
    l8_vis_params_cir,
    "Landsat 8 - CIR - 2018 - RMNP - Snow Off",
)

# Add RMNP boundary to map
rmnp_map.addLayer(rmnp_boundary_vis, {"palette": "FF0000"}, "RMNP Boundary")
```

```{code-block} python
# Display map
rmnp_map
```

## Data Export
```{code-block} python
# No data processing in this lab.
```

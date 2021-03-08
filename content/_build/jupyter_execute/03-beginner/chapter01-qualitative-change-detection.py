# Chapter 1: Qualitative Change Detection

## Background

One of the central values of long-term remote sensing programs is the opportunity to study the changing nature of the land surface. With nearly 9 billion people on the planet, we have a wide array of opportunities to study man-induced change as well as change related to natural land surface processes. The nearly 40-year record of the Landsat program and the growing collections from the National Aeronautics and Space Administration (NASA) Earth Observing System (EOS) Moderate Resolution Imaging Spectroradiometer (MODIS) platform and the European Space Agency (ESA) Sentinel platforms provide great opportunities to discover where long-term change is occurring on Earth's surface. 

This chapter introduces a simple, image algebra-based approached to change detection. As in Equation {eq}`equation:1`, one date is subtracted from another and a constant is added in the equation so that you end up with a range of positive values in your difference image. 

```{math}
:label: equation:1

change = date_{2} – date_{1} + constant
```

The image histogram for the difference image may then be interpreted to discover where pixels have changes. Those pixels lying closest to the center of the histogram are least likely to have changed, while those in the "tails" of the histogram represent those pixels most likely to have changed between the two image dates. High-resolution imagery, like that found in the GEE Collection of the National Agriculture Imagery Program (NAIP), can be used to aid in the interpretation of the difference image.

## Environment Setup

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

# Initialize Earth Engine Python API
initialize_earth_engine()

# Import geemap
import_geemap()

## Data Acquisition and Preprocessing

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

## Data Processing

# No data processsing in this chapter.

## Data Postprocessing

# No data postprocessing in this chapter.

## Data Visualization

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

# Display map
rmnp_map

## Data Export

# No data export in this chapter.
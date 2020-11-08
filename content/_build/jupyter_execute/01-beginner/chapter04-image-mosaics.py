# Chapter 4: Image Mosaics

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

# Get boundary for Rocky Mountain National Park, Colorado (from GEE Asset)
vt_boundary = ee.FeatureCollection(
    "users/calekochenour/vermont_state_boundary"
)

# Get Landsat 8 collection
landsat8_t1_sr = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")

# Filter Landsat 8 to least cloudy in September
vermont_summer_median = (
    landsat8_t1_sr.filter(ee.Filter.calendarRange(2013, 2020, "year"))
    .filter(ee.Filter.calendarRange(6, 9, "month"))
    .filterBounds(vt_boundary)
    .filterMetadata("CLOUD_COVER", "less_than", 0.45)
    .median()
    .clip(vt_boundary)
)

# Load and clip the Hansen dataset
hansen_2015 = ee.Image("UMD/hansen/global_forest_change_2015").clip(
    vt_boundary
)

# Select the mask band
datamask = hansen_2015.select("datamask")

# Create the binary mask; non-water features, no data (0) and land (1)
# Select water (2) features; water will get value of 1 (used to mask),
#   and no data and land will get values of 0 (don't mask)
water = datamask.eq(2)

# Create water image (mask water with itself); returns only water objects
#  that had mask values of 1
water = water.mask(water)

## Data Processing

# No data processsing in this chapter.

## Data Postprocessing

# No data postprocessing in this chapter.

## Data Visualization

# Create interactive map for visualization and set options
if "vermont_map" in globals():
    del vermont_map
    vermont_map = gm.Map()
    vermont_map.setOptions("SATELLITE")
    vermont_map.setCenter(lon=-72.7330, lat=44.0939, zoom=7)
else:
    vermont_map = gm.Map()
    vermont_map.setOptions("SATELLITE")
    vermont_map.setCenter(lon=-72.7330, lat=44.0939, zoom=7)

# Create visualization image for Landsat 8 median composite
vermont_vis_rgb = vermont_summer_median.visualize(
    **{"bands": ["B4", "B3", "B2"], "min": 0, "max": 2000}
)

# Create visualization image for Hansen water mask
water_vis = water.visualize(
    **{"palette": "blue", "max": 1, "min": 0, "opacity": 0.75}
)

# Create mosaic from image visualizations
vermont_mosaic = ee.ImageCollection([vermont_vis_rgb, water_vis]).mosaic()
vt_boundary_vis = (
    ee.Image()
    .byte()
    .paint(**{"featureCollection": vt_boundary, "color": 1, "width": 3})
)

# Add indiviual visualizations to map
vermont_map.addLayer(vermont_vis_rgb, {}, "Vermont Median RGB Visualization")
vermont_map.addLayer(water_vis, {}, "Vermont Water Visualization")

# Add mosiac to map
vermont_map.addLayer(vermont_mosaic, {}, "Vermont RGB & Water Mosaic")

# Add RMNP boundary to map
vermont_map.addLayer(
    vt_boundary_vis, {"palette": "FF0000"}, "Vermont Boundary"
)

# Display map
vermont_map

## Data Export

# No data export in this chapter.
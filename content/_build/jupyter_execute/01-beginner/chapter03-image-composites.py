# Chapter 3: Image Composites

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

# Load Notebook formatter
%load_ext nb_black

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

## Data Acquisition and Preprocessing

# Get boundary for Rocky Mountain National Park, Colorado
rmnp_boundary = ee.FeatureCollection(
    "users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon"
)

# Filter Sentinel-2 imagery for summer 2018
rmnp_summer_2018 = (
    ee.ImageCollection("COPERNICUS/S2_SR")
    .filterDate("2019-06-01", "2019-09-30")
    .filterBounds(rmnp_boundary)
)
# rmnp_summer_2018.getInfo()

## Data Processing

# Create composite images
rmnp_summer_2018_mean = rmnp_summer_2018.mean().clip(rmnp_boundary)
rmnp_summer_2018_median = rmnp_summer_2018.median().clip(rmnp_boundary)
rmnp_summer_2018_max = rmnp_summer_2018.max().clip(rmnp_boundary)
rmnp_summer_2018_min = rmnp_summer_2018.min().clip(rmnp_boundary)

## Data Postprocessing

No data postprocessing in this chapter.

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

# Set visualization parameters
s2_vis_params_rgb = {"bands": ["B4", "B3", "B2"], "min": 0, "max": 3000}
vis_params_ndvi = {"min": -1, "max": 1, "palette": ["blue", "white", "green"]}

# Set RMNP boundary visualization parameters
rmnp_boundary_vis = (
    ee.Image()
    .byte()
    .paint(**{"featureCollection": rmnp_boundary, "color": 1, "width": 3})
)

# Add composite images
rmnp_map.addLayer(
    ee_object=rmnp_summer_2018_mean,
    vis_params=s2_vis_params_rgb,
    name="Sentinel 2 - RGB - Summer 2018 - RMNP - Mean",
    opacity=1.0,
)

rmnp_map.addLayer(
    rmnp_summer_2018_median,
    s2_vis_params_rgb,
    "Sentinel 2 - RGB - Summer 2018 - RMNP - Median",
)

rmnp_map.addLayer(
    rmnp_summer_2018_max,
    s2_vis_params_rgb,
    "Sentinel 2 - RGB - Summer 2018 - RMNP - Max",
)

rmnp_map.addLayer(
    rmnp_summer_2018_min,
    s2_vis_params_rgb,
    "Sentinel 2 - RGB - Summer 2018 - RMNP - Min",
)

# Add RMNP boundary to map
rmnp_map.addLayer(rmnp_boundary_vis, {"palette": "FF0000"}, "RMNP Boundary")

# Display map
rmnp_map

## Data Export

No data export in this chapter.
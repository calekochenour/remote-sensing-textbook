# Chapter 6: Cloud Masking

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

def mask_clouds_shadows_landsat8(image):
    """Masks clouds and cloud shadows in a Landsat 8 image.
    
    Parameters
    ----------
    image : ee.image.Image object
        Landsat 8 image.
    
    Returns
    -------
    masked_image : ee.image.Image object
         Input image masked for clouds and cloud shadows.
    
    Example
    -------
        >>>
        >>>
        >>>
        >>>
    """
    # Define cloud shadow (3) and cloud (5) mask bits
    cloud_shadow_bit_mask = 1 << 3
    cloud_bit_mask = 1 << 5

    # Get the pixel QA band
    qa = image.select("pixel_qa")

    # Create mask image, based on both bit masks == 0
    mask = qa.bitwiseAnd(cloud_shadow_bit_mask).eq(0) and qa.bitwiseAnd(
        cloud_bit_mask
    ).eq(0)

    # Mask image
    masked_image = image.updateMask(mask)

    return masked_image

def clip_to_rmnp(image):
    """Helper function to clip an image to the RMNP boundary.
    """
    # Clip image to RMNP boundary
    clipped = image.clip(rmnp_boundary)

    return clipped

# Initialize Earth Engine Python API
initialize_earth_engine()

# Import geemap
import_geemap()

## Data Acquisition and Preprocessing

# Get RMNP boundary
rmnp_boundary = ee.FeatureCollection(
    "users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon"
)

# Create mean composite of unmasked images for summer 2013-2020
rmnp_unmasked_mean = (
    ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
    .filter(ee.Filter.calendarRange(2013, 2020, "year"))
    .filter(ee.Filter.calendarRange(6, 9, "month"))
    .filterBounds(rmnp_boundary)
    .map(clip_to_rmnp)
    .mean()
)

# Create mean composite of masked images for summer 2013-2020
rmnp_masked_mean = (
    ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
    .filter(ee.Filter.calendarRange(2013, 2020, "year"))
    .filter(ee.Filter.calendarRange(6, 9, "month"))
    .filterBounds(rmnp_boundary)
    .map(clip_to_rmnp)
    .map(mask_clouds_shadows_landsat8)
    .mean()
)

## Data Processing

# No data processing in this chapter.

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

# Set visualization parameters, Landsat 8 RGB and CIR
l8_vis_params_rgb = {"bands": ["B4", "B3", "B2"], "min": 0, "max": 3000}
l8_vis_params_cir = {"bands": ["B5", "B4", "B3"], "min": 0, "max": 3000}

# Add unmasked and masked composites
rmnp_map.addLayer(
    rmnp_unmasked_mean,
    l8_vis_params_rgb,
    "Landsat 8 - RGB - RMNP Unmasked Mean Composite",
)

rmnp_map.addLayer(
    rmnp_masked_mean,
    l8_vis_params_rgb,
    "Landsat 8 - RGB - RMNP Masked Mean Composite",
)

rmnp_map.addLayer(
    rmnp_unmasked_mean,
    l8_vis_params_cir,
    "Landsat 8 - CIR - RMNP Unmasked Mean Composite",
)

rmnp_map.addLayer(
    rmnp_masked_mean,
    l8_vis_params_cir,
    "Landsat 8 - CIR - RMNP Masked Mean Composite",
)

# Display map
rmnp_map

## Data Export

# No data export in this chapter.
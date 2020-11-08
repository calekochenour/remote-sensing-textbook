# Chapter 2: Normalized Difference

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
co_snow_on_2018_l8 = (
    landsat8_t1_sr.filterDate("2018-03-01", "2018-04-30")
    .filterBounds(rmnp_boundary)
    .sort("CLOUD_COVER")
    .first()
)

# Filter Landsat 8 Tier 1 SR to snow-off conditions near RMNP, 2018
co_snow_off_2018_l8 = (
    landsat8_t1_sr.filterDate("2018-07-01", "2018-08-31")
    .filterBounds(rmnp_boundary)
    .sort("CLOUD_COVER")
    .first()
)

# Clip snow-on and snow-off imagery to RMNP boundary
rmnp_snow_on_2018_l8 = co_snow_on_2018_l8.clip(rmnp_boundary)
rmnp_snow_off_2018_l8 = co_snow_off_2018_l8.clip(rmnp_boundary)

# Get Sentinel-2 collection
sentinel2_level2a = ee.ImageCollection("COPERNICUS/S2_SR")

# Filter Sentinel-2 Level 2A to snow-on conditions near RMNP, 2019
co_snow_on_2019_s2 = (
    sentinel2_level2a.filterDate("2019-03-01", "2019-04-30")
    .filterBounds(rmnp_boundary)
    .sort("CLOUDY_PIXEL_PERCENTAGE")
    .first()
)

# Get list of all bands
s2_band_names = co_snow_on_2019_s2.bandNames()

# Get a specific band(s)
s2_red = co_snow_on_2019_s2.select("B4")
s2_red_nir = co_snow_on_2019_s2.select(["B4", "B8"])

# Get a list of all metadata properties
s2_properties = co_snow_on_2019_s2.propertyNames()

# Get a specific metadata property
cloudiness = co_snow_on_2019_s2.get("CLOUD_COVERAGE_ASSESSMENT")

# Get a specific metadata property
cloudiness = co_snow_on_2019_s2.get("CLOUDY_PIXEL_PERCENTAGE")

# Get the timestamp and convert to date
date = ee.Date(co_snow_on_2019_s2.get("system:time_start"))

# Filter Sentinel-2 Level 2A to snow-off conditions near RMNP, 2019
co_snow_off_2019_s2 = (
    sentinel2_level2a.filterDate("2019-07-01", "2019-08-31")
    .filterBounds(rmnp_boundary)
    .sort("CLOUDY_PIXEL_PERCENTAGE")
    .first()
)

# Clip snow-on and snow-off imagery (Sentinel-2) to RMNP boundary
rmnp_snow_on_2019_s2 = co_snow_on_2019_s2.clip(rmnp_boundary)
rmnp_snow_off_2019_s2 = co_snow_off_2019_s2.clip(rmnp_boundary)

## Data Processing

# Calculate NDVI for Landsat 8
rmnp_ndvi_snow_on_l8 = co_snow_on_2018_l8.normalizedDifference(
    ["B5", "B4"]
).clip(rmnp_boundary)

rmnp_ndvi_snow_off_l8 = co_snow_off_2018_l8.normalizedDifference(
    ["B5", "B4"]
).clip(rmnp_boundary)

# Calculate NDVI for Sentinel-2
rmnp_ndvi_snow_on_s2 = co_snow_on_2019_s2.normalizedDifference(
    ["B8", "B4"]
).clip(rmnp_boundary)

rmnp_ndvi_snow_off_s2 = co_snow_off_2019_s2.normalizedDifference(
    ["B8", "B4"]
).clip(rmnp_boundary)

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
l8_vis_params_rgb = {"bands": ["B4", "B3", "B2"], "min": 0, "max": 3000}
l8_vis_params_cir = {"bands": ["B5", "B4", "B3"], "min": 0, "max": 3000}
s2_vis_params_rgb = {"bands": ["B4", "B3", "B2"], "min": 0, "max": 3000}
s2_vis_params_cir = {"bands": ["B8", "B4", "B3"], "min": 0, "max": 3000}
vis_params_ndvi = {"min": -1, "max": 1, "palette": ["blue", "white", "green"]}

# Set RMNP boundary visualization parameters
rmnp_boundary_vis = (
    ee.Image()
    .byte()
    .paint(**{"featureCollection": rmnp_boundary, "color": 1, "width": 3})
)

# Add snow-on and snow-off images to map, Landsat 8, RGB and CIR
rmnp_map.addLayer(
    rmnp_snow_on_2018_l8,
    l8_vis_params_rgb,
    "Landsat 8 - RGB - 2018 - RMNP - Snow On",
)

rmnp_map.addLayer(
    rmnp_snow_on_2018_l8,
    l8_vis_params_cir,
    "Landsat 8 - CIR - 2018 - RMNP - Snow On",
)

rmnp_map.addLayer(
    rmnp_snow_off_2018_l8,
    l8_vis_params_rgb,
    "Landsat 8 - RGB - 2018 - RMNP - Snow Off",
)

rmnp_map.addLayer(
    rmnp_snow_off_2018_l8,
    l8_vis_params_cir,
    "Landsat 8 - CIR - 2018 - RMNP - Snow Off",
)

# Add snow-on and snow-off images to map, Sentinel-2, RGB and CIR
rmnp_map.addLayer(
    rmnp_snow_on_2019_s2,
    s2_vis_params_rgb,
    "Sentinel-2 - RGB - 2019 - RMNP - Snow On",
)

rmnp_map.addLayer(
    rmnp_snow_on_2019_s2,
    s2_vis_params_cir,
    "Sentinel-2 - CIR - 2019 - RMNP - Snow On",
)

rmnp_map.addLayer(
    rmnp_snow_off_2019_s2,
    s2_vis_params_rgb,
    "Sentinel-2 - RGB - 2019 - RMNP - Snow Off",
)

rmnp_map.addLayer(
    rmnp_snow_off_2019_s2,
    s2_vis_params_cir,
    "Sentinel-2 - CIR - 2019 - RMNP - Snow Off",
)

# Add NDVI to map
rmnp_map.addLayer(
    rmnp_ndvi_snow_on_l8,
    vis_params_ndvi,
    "Landsat 8 - NDVI - 2018 - RMNP - Snow On",
)

rmnp_map.addLayer(
    rmnp_ndvi_snow_off_l8,
    vis_params_ndvi,
    "Landsat 8 - NDVI - 2018 - RMNP - Snow Off",
)

rmnp_map.addLayer(
    rmnp_ndvi_snow_on_s2,
    vis_params_ndvi,
    "Sentinel-2 - NDVI - 2019 - RMNP - Snow On",
)

rmnp_map.addLayer(
    rmnp_ndvi_snow_off_s2,
    vis_params_ndvi,
    "Sentinel-2 - NDVI - 2019 - RMNP - Snow Off",
)

# Add RMNP boundary to map
rmnp_map.addLayer(rmnp_boundary_vis, {"palette": "FF0000"}, "RMNP Boundary")

# Display map
rmnp_map

## Data Export

No data export in this chapter.
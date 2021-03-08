# Chapter 5: Image Collection Iteration

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

def accumulate(image, image_list):
    """
    Parameters
    ----------
    image : ee.image.Image object
        Landsat 8 image.
        
    image_list : ee.ee_list.List object
        List with initialized image.
    
    Returns
    -------
    cumulative_list : ee.ee_list.List object
        Input listt with the cumulative anomaly added.
    
    Example
    -------
        >>>
        >>>
        >>>
        >>>
    """
    # Get the latest cumulative anomaly image from the end of the list with
    #  get(-1). Since the type of the list argument to the function is unknown,
    #  it needs to be cast to a List. Since the return type of get() is
    #  unknown, cast it to Image
    previous = ee.Image(ee.List(image_list).get(-1))

    # Add the current anomaly to make a new cumulative anomaly image,
    #  propagate metadata to the new image
    added = image.add(previous).set(
        "system:time_start", image.get("system:time_start")
    )

    # Get final list
    cumulative_list = ee.List(image_list).add(added)

    return cumulative_list

def clip_to_rmnp(image):
    """Helper function for the NDVI difference accumulation.
    """
    # Clip image to RMNP boundary
    clipped = image.clip(rmnp_boundary)

    return clipped

def subtract_ndvi_mean(image):
    """Helper function for the NDVI difference accumulation.
    """
    # Subtract NDVI mean from image
    subtracted = image.subtract(rmnp_summer_ndvi_mean).set(
        "system:time_start", image.get("system:time_start")
    )

    return subtracted

# Initialize Earth Engine Python API
initialize_earth_engine()

# Import geemap
import_geemap()

## Data Acquisition and Preprocessing

# Set boundary for Rocky Mountain National Park, Colorado (from GEE Asset)
rmnp_boundary = ee.FeatureCollection(
    "users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon"
)

# Get Landsat 8 collection
landsat8_t1_sr = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")

# Add NDVI band to each image in the collection (with mapping)
landsat8_t1_sr_ndvi = landsat8_t1_sr.map(add_ndvi).select("NDVI")

# Filter Landsat 8 NDVI collection for June-September for 2013-2018
#  (baseline/reference data)
rmnp_summer_ndvi = (
    landsat8_t1_sr_ndvi.filter(ee.Filter.calendarRange(2013, 2018, "year"))
    .filter(ee.Filter.calendarRange(6, 9, "month"))
    .filterBounds(rmnp_boundary)
    .sort("system:time_start", False)
)

## Data Processing

# Compute mean for the entire NDVI collection; clip to RMNP
rmnp_summer_ndvi_mean = rmnp_summer_ndvi.mean().clip(rmnp_boundary)

# Compute NDVI difference (image - reference mean) series for all images
#  post-baseline (2019-2020)
rmnp_ndvi_diff_series = (
    landsat8_t1_sr_ndvi.filter(ee.Filter.calendarRange(2019, 2020, "year"))
    .filter(ee.Filter.calendarRange(6, 9, "month"))
    .filterBounds(rmnp_boundary)
    .map(clip_to_rmnp)
    .map(subtract_ndvi_mean)
)

# Compute min and max accumulated NDVI difference (for plotting min/max)
ndvi_diff_min = ee.Number(
    rmnp_ndvi_diff_series.sum()
    .reduceRegion(
        **{
            "reducer": ee.Reducer.min(),
            "geometry": rmnp_boundary.geometry(),
            "scale": 30,
            "maxPixels": 1e9,
        }
    )
    .get("NDVI")
)

ndvi_diff_max = ee.Number(
    rmnp_ndvi_diff_series.sum()
    .reduceRegion(
        **{
            "reducer": ee.Reducer.max(),
            "geometry": rmnp_boundary.geometry(),
            "scale": 30,
            "maxPixels": 1e9,
        }
    )
    .get("NDVI")
)

# Get the timestamp from the most recent image in the reference collection
time_0 = rmnp_summer_ndvi.first().get("system:time_start")

print(f"Minimum Accumulated NDVI Difference: {ndvi_diff_min.getInfo()}")
print(f"Maximum Accumulated NDVI Difference: {ndvi_diff_max.getInfo()}")
print(f"Time Zero: {time_0.getInfo()}")

# Initialize difference (anomaly) accumulation to 0 (image with all 0s and
#  timestamp time_0); rename the first band from 'constant' (default) to 'NDVI'
initialized_accumulation = ee.List(
    [
        ee.Image(0)
        .set("system:time_start", time_0)
        .select([0], ["NDVI"])
        .clip(rmnp_boundary)
    ]
)

print(f"Initialzed accumulation: {initialized_accumulation.getInfo()}")
print(f"Type: {initialized_accumulation.name()}")

# Create an ImageCollection of cumulative anomaly images (NDVI differences)
# Cast return object of .iterate() to type List, as it is by default unknown
#  (ComputedObject)
# .iterate() takes a function as param 1 and the initial state as param 2
ndvi_diff_cumulative = ee.ImageCollection(
    ee.List(
        rmnp_ndvi_diff_series.iterate(accumulate, initialized_accumulation)
    )
)

print(
    f"Accumulated collection via iteration: {ndvi_diff_cumulative.getInfo()}"
)
print(
    f"Accumulated collection via iteration type: {ndvi_diff_cumulative.name()}"
)

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

# Set visualization parameters
vis_params_ndvi = {"min": -1, "max": 1, "palette": ["blue", "white", "green"]}

# Set RMNP boundary visualization parameters
rmnp_boundary_vis = (
    ee.Image()
    .byte()
    .paint(**{"featureCollection": rmnp_boundary, "color": 1, "width": 3})
)

# Add layers to map
rmnp_map.addLayer(
    rmnp_summer_ndvi_mean,
    vis_params_ndvi,
    "Landsat 8 - NDVI Mean - Jun/Sep 2013/2020",
)

# Display accumulated NDVI differences (anomalies from 6-year mean)
rmnp_map.addLayer(
    rmnp_ndvi_diff_series.sum(),
    {
        "min": -2.5899382242647437,
        "max": 2.548139614675886,
        "palette": ["FF0000", "000000", "00FF00"],
    },
    "Cumulative NDVI Difference",
)

# Add RMNP boundary to map
rmnp_map.addLayer(rmnp_boundary_vis, {"palette": "FF0000"}, "RMNP Boundary")

# Display map
rmnp_map

## Data Export

# No data export in this chapter.
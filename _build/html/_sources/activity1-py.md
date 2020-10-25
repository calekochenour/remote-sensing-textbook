# Python

The purpose of this lesson is to review the change from leaf-off imagery to leaf-on imagery for a study areas of interest.  

In this lesson, you will:

* Choose an area and Landsat collection of interest;
* Filter the Landsat collection to obtain leaf-off and leaf-on imagery; and,
* Display a single image from both leaf-off and leaf-on conditions.

## Environment Setup
```{code-block} python
# Import packages
import ee
import geemap as gm

# Initialze GEE Python API; authenticate if necessary
try:
    ee.Initialize()

except Exception as error:
    ee.Authenticate()
    ee.Initialize()
```

## Data Acquisition & Pre-Processing
```{code-block} python
# Define boundary for Rocky Mountain National Park, Colorado
rmnp_boundary = ee.FeatureCollection(
    "users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon")

# Define Landsat 8 collection
landsat8_t1_sr = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')

# Filter Landsat 8 Tier 1 SR to snow-on conditions near RMNP, 2018
co_snow_on_2018 = landsat8_t1_sr.filterDate(
    '2018-03-01', '2018-04-30').filterBounds(
    rmnp_boundary).sort('CLOUD_COVER').first()

# Filter Landsat 8 Tier 1 SR to snow-off conditions near RMNP, 2018
co_snow_off_2018 = landsat8_t1_sr.filterDate(
    '2018-07-01', '2018-08-31').filterBounds(
    rmnp_boundary).sort('CLOUD_COVER').first()

# Clip snow-on and snow-off imagery to RMNP boundary
rmnp_snow_on_2018 = co_snow_on_2018.clip(rmnp_boundary)
rmnp_snow_off_2018 = co_snow_off_2018.clip(rmnp_boundary)
```

## Data Processing
```{code-block} python
# No data processing in this lab.
```

## Data Visualization
```{code-block} python
# Define Landsat 8 RGB visualization parameters
l8_vis_params_rgb = {
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 3000
}

# Define Landsat 8 CIR visualization parameters
l8_vis_params_cir = {
  'bands': ['B5', 'B4', 'B3'],
  'min': 0,
  'max': 3000
}

# Define RMNP boundary visualization parameters
empty = ee.Image().byte()

rmnp_boundary_vis = empty.paint(
    featureCollection=rmnp_boundary, color=1, width=3)
```

```{code-block} python
# Create map for visualization
rmnp_snow_map = gm.Map()
rmnp_snow_map.setOptions('SATELLITE')

# Center map to Rocky Mountain National Park, Colorado
rmnp_snow_map.setCenter(-105.6836, 40.3428, 10)
```

```{code-block} python
# Add snow-on and snow-off images to map, RGB and CIR
rmnp_snow_map.addLayer(
    rmnp_snow_on_2018,
    l8_vis_params_rgb,
    'Landsat 8 - RGB - 2018 - Snow On')

rmnp_snow_map.addLayer(
    rmnp_snow_on_2018,
    l8_vis_params_cir,
    'Landsat 8 - CIR - 2018 - Snow On')

rmnp_snow_map.addLayer(
    rmnp_snow_off_2018,
    l8_vis_params_rgb,
    'Landsat 8 - RGB - 2018 - Snow Off')

rmnp_snow_map.addLayer(
    rmnp_snow_off_2018,
    l8_vis_params_cir,
    'Landsat 8 - CIR - 2018 - Snow Off')

# Add RMNP boundary to map
rmnp_snow_map.addLayer(
    rmnp_boundary_vis,
    {'palette': 'FF0000'},
    'RMNP Boundary')
```

```{code-block} python
# Display map
rmnp_snow_map
```

## Data Export
```{code-block} python
# No data export in this lab.
```

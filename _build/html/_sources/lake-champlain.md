# Lake Champlain

## Introduction

The purpose of this lesson is to further extend your knowledge of GEE and functions to bring images and image collections into the browser for further analysis.

You’ll locate a Landsat image in any area on the planet that interests you. It could be some place you've lived, visited, or a place where you've worked. It's your choice. You can use the map (at the bottom of the Code Editor). In the upper left corner there are drawing tools to allow you to define polygons on the map interface below the Code Editor window.

## Lesson Steps

### 0. Set Up GEE Environment

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

### 1. Chose an Area of Interest

Define a study area of interest.

Hint: Point or polygon geometry should suffice. Review the EE [Geometry Overview](https://developers.google.com/earth-engine/geometries#creating-geometry-objects).

```{code-block} python
# Define point for the center of Lake Champlain, Vermont
lake_champlain_center = ee.Geometry.Point(-73.3333, 44.5333)
```

```{code-block} python
# DO NOT MODIFY - AUTOGRADE
# Initialize points
points = 0

# Check if type is EE geometry
try:
    assert isinstance(lake_champlain_center, ee.geometry.Geometry)
    print("Your study area is the correct type - ee.geometry.Geometry")
    points += 10

# Catch assertion error
except AssertionError as error:
    print("AssertionError:",
          "Your study area object should be of type ee.geometry.Geometry.")

# Show points earned    
print(f"Points earned: {points}")
```

### 2. Import a Landsat Collection

Use the `ee.ImageCollection` ("Name of Collection") function.

Hint: In the EE DataCatalog each collection has an "EE Snippet" of code that you can cut-and-paste. You can choose any of the Landsat Tier-1 Collections (more on collections that are in the Data Catalog later).


```{code-block} python
# Define collection
landsat8_t1_sr = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
```

```{code-block} python
# DO NOT MODIFY - AUTOGRADE
# Initialize points
points = 0

# Check if type is EE image collection
try:
    assert isinstance(landsat8_t1_sr, ee.imagecollection.ImageCollection)
    print("Your image collection object is the correct type - ee.imagecollection.ImageCollection")
    points += 10

# Catch assertion error
except AssertionError as error:
    print("AssertionError:",
          "Your image collection object should be of type ee.imagecollection.ImageCollection.")

# Show points earned
print(f"Points earned: {points}")
```

### 3. Filter the Collection to a Specific Time Period

Use the various `.filter` methods under `ee.collection` to filter your data. See examples [here](https://developers.google.com/earth-engine/ic_filtering).

For instance:

```{code-block} python
reduced_collection = ee.ImageCollection(
    'LANDSAT/LT05/C01/T2').filterDate('1987-01-01', '1990-05-01')
```

You can filter on time and location, image quality, and numerous other image collection properties.

For now just choose a time range and a location (use `.filterbounds` for this step).

```{code-block} python
# Filter Landsat 8 Tier 1 SR to Vermont, 6/2018-9/2018
vermont_jun_sep_2018 = landsat8_t1_sr.filterDate(
    '2018-06-01', '2018-09-30').filterBounds(lake_champlain_center)
```

```{code-block} python
# DO NOT MODIFY - AUTOGRADE
# Initialize points
points = 0

# Check if filtered collection is reduced (less images than original)
try:
    assert vermont_jun_sep_2018.size().getInfo() < landsat8_t1_sr.size().getInfo()
    print("Your filtered image collection object has been reduced.")
    points += 10

# Catch assertion error
except AssertionError as error:
    print("AssertionError:",
          "Your filtered image collection object has not been reduced."
          "It has the same number of images as the original collection.")

# Show points earned
print(f"Points earned: {points}")
```

    Your filtered image collection object has been reduced.
    Points earned: 10

### 4. Apply the Palette to Improve your Visualizations

Recall that you used the EE palette in Lesson 1, feel free to re-use that code in this exercise. More information on the palette and visualizing imagery can be found [here](https://developers.google.com/earth-engine/tutorial_api_02). You should use the palette to help you visualize your outputs in this exercise.

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
  'max': 5000
}
```

```{code-block} python
# DO NOT MODIFY - AUTOGRADE
# Initialize points
points = 0

# Check if vis params have the correct bands for Landsat 8
try:
    assert l8_vis_params_rgb.get('bands') == ['B4', 'B3', 'B2']
    print("Your RGB visualization parameters have the correct bands.")
    points += 10

# Catch assertion error
except AssertionError as error:
    print("AssertionError:",
          "Your RGB visualization parameters have incorrect bands.")

# Show points earned
print(f"Points earned: {points}")
```

### 5. "Reduce" Your Collection by Compositing Imagery

Using filters above helps to "reduce" the number of scenes in a collection that you're working with. However this can still result in a "ton" of data! You can use compositing, as described [here](https://developers.google.com/earth-engine/tutorial_api_05), to calculate across all of the images (and bands) in your filtered collection to create, for example, a "median" image. Recall your basic statistics: the median is the "middle value" in a set of observations. Other measures could be applied here too, for instance the "mean" across all images could be determined.

For this part of the exercise take your time- and space-filtered collection from above and apply a reducer like the "median". One of the things to remember about collections and display is that the default display on the map for a collection is to take the very latest image in the collection and display. Reducing to the median allows you to "composite" all of the images in the collection and display this result.

```{code-block} python
# Sort collection from least to most cloudy
vermont_sorted = vermont_jun_sep_2018.sort('CLOUD_COVER')

# Reduce collection to the first (least cloudy) image
vermont_least_cloudy = ee.Image(vermont_sorted.first())
```

```{code-block} python
# DO NOT MODIFY - AUTOGRADE
# Initialize points
points = 0

# Check if image collection has been reduced to a single image
try:
    assert vermont_least_cloudy.getInfo().get('type') == 'Image'
    print("Your image collection has been reduced to a single image.")
    points += 10

# Catch assertion error
except AssertionError as error:
    print("AssertionError:",
          "Your image collection has not been reduced to a single image.")

# Show points earned
print(f"Points earned: {points}")
```

### 6. Create a Map of the Composite Image

Combine the visualization parameters with your composite image to add the composite to an interactive map for viewing.

Hint: Review the [Image Visualization](https://developers.google.com/earth-engine/image_visualization) documentation, specifically the `Map.addLayer()` function, for help with adding layers to an EE map.

Hint: Run the following commands in Jupyter Notebook to review `geemap` documentation for creating and working with an interactive map in Python:

```{code-block} python
# Call help on geemap class and methods
help(gm.Map)
help(gm.Map.setOptions)
help(gm.Map.setCenter)
help(gm.Map.addLayer)
```

Hint: To display a map within Jupyter Notebook, first create a `geemap.Map` object, configure options,  and add layers, then call the variable containing the `geemap.Map` object:

```{code-block} python
# Instantiate map object
ee_map = gm.Map()

# Configure map options
# CODE FOR MAP OPTIONS

# Add layers to map
# CODE FOR MAP LAYERS

# Display map
ee_map
```

```{code-block} python
# Create interactive map for visualization
vermont_map = gm.Map()

# Set basemap
vermont_map.setOptions('SATELLITE')

# Center map to study area
vermont_map.setCenter(
    lon=lake_champlain_center.coordinates().getInfo()[0],
    lat=lake_champlain_center.coordinates().getInfo()[1],
    zoom=8)
```

```{code-block} python
# Add least cloudy, RGB and CIR to interactive map
vermont_map.addLayer(
    ee_object=vermont_least_cloudy,
    vis_params=l8_vis_params_rgb,
    name="Vermont | Lake Champlain | Least Cloudy | RGB",
    shown=True,
    opacity=1)

vermont_map.addLayer(
    ee_object=vermont_least_cloudy,
    vis_params=l8_vis_params_cir,
    name="Vermont | Lake Champlain | Least Cloudy | CIR",
    shown=True,
    opacity=1)

# Add study area (point) to map
vermont_map.addLayer(
    ee_object=lake_champlain_center,
    vis_params={'color': '00FF00', 'width': 5},
    name='Vermont | Lake Champlain | Center',
    shown=True,
    opacity=1)
```

```{code-block} python
# Display map
vermont_map
```

### 7. Apply Masking and Mosaicking Functions

Masks and mosaics (information found [here](https://developers.google.com/earth-engine/tutorial_api_05)) are very traditional image processing functions. GEE provides very nice capabilities to customize outputs. Read through the example provided and apply a similar approach to your reduced collection. The example discusses a "water mask", but there are other ways to mask an image, like for instance using a polygon coverage of political boundaries, or maybe "ecoregions". Try your hand at applying the water mask or developing your own mask, and then use the mosaic function to combine the mask and the reduced image. Hint: There are ancillary data resources in the data catalog that could be used in this step.

```{code-block} python
# Load the Hansen dataset
hansen_2015 = ee.Image('UMD/hansen/global_forest_change_2015')

# Select the mask band
datamask = hansen_2015.select('datamask')

# Create the binary mask; non-water features, no data (0) and land (1)
water = datamask.eq(2)

# Create water image (mask water with itself)
water = water.mask(water)
```

```{code-block} python
# Create visualization image for Landsat 8
vermont_least_cloudy_rgb = vermont_least_cloudy.visualize(
    **{'bands': ['B4', 'B3', 'B2'], 'max': 3000, 'min': 0})

# Create visualization image for Hansen water mask
water_vis = water.visualize(
    **{'palette': 'blue', 'max': 1, 'min': 0, 'opacity': 0.75})
```

```{code-block} python
# Get Landsat image boundary coordinates
landsat_image_coords = vermont_least_cloudy.getInfo().get(
    'properties').get('system:footprint').get('coordinates')

# Define Landsat clip polygon from coordinates
vermont_clip_poly = ee.Geometry.Polygon([landsat_image_coords])

# Clip water mask to Landsat polygon
water_vis_clip = water_vis.clip(vermont_clip_poly)
```

```{code-block} python
# Create image collection from image visualizations
vermont_collection = ee.ImageCollection(
    [vermont_least_cloudy_rgb, water_vis_clip])

# Create mosaic from image collection
vermont_mosaic = vermont_collection.mosaic()
```

### 8. Create a Map of the Mosaic Image

Create a new interactive map and add the mosaic image to the map for viewing.

Hint: Follow the guidance provided in Section 6 for creating and configuring an interactive map in Jupyter Notebook.

```{code-block} python
# Create interactive map for visualization
mosaic_map = gm.Map()

# Set basemap
mosaic_map.setOptions('SATELLITE')

# Center map to study area
mosaic_map.setCenter(
    lon=lake_champlain_center.coordinates().getInfo()[0],
    lat=lake_champlain_center.coordinates().getInfo()[1],
    zoom=8)
```

```{code-block} python
# Add mosaic image to the map
mosaic_map.addLayer(vermont_mosaic, {}, 'Vermont | Lake Champlain | Water Mask Mosaic');
```

```{code-block} python
# Display map
mosaic_map
```

# Chapter 9: Image Composites

This chapter provides a workflow to create composite images from a collection of Summer imagery in Rocky Mountain National Park, Colorado, United States. The full GEE code can be found [here](https://code.earthengine.google.com/2528a4c2c3910aa9557447174adaf33a).

## Functions

```{code-block} javascript
/**
 * Calculate and add NDVI band to Landsat 8 image
 * @param  {ee.Image} image - Landsat 8 image
 * @return {ee.Image}       - Landsat 8 image with NDVI band added
 */
var add_ndvi = function(image) {
  var ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI');
  return image.addBands(ndvi);
};
```

## Data Acquisition & Preprocessing

```{code-block} javascript
// Define boundary for Rocky Mountain National Park, Colorado (from GEE Asset)
var rmnp_boundary = ee.FeatureCollection("users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon");
// print(rmnp_boundary);

// Define Sentinel-2 collection
var sentinel2_level2a = ee.ImageCollection("COPERNICUS/S2_SR");

// Filter Sentinel-2
var rmnp_summer_2018 = sentinel2_level2a
  .filterDate('2019-06-01', '2019-09-30')
  .filterBounds(rmnp_boundary);
print('RMNP Summer 2018: ', rmnp_summer_2018);
```

## Data Processing

```{code-block} javascript
// Add NDVI band to each image in the collection (with mapping)
rmnp_summer_2018 = rmnp_summer_2018.map(add_ndvi);
print(rmnp_summer_2018);

// Create composite images
var rmnp_summer_2018_mean = rmnp_summer_2018.mean().clip(rmnp_boundary);
var rmnp_summer_2018_median = rmnp_summer_2018.median().clip(rmnp_boundary);
var rmnp_summer_2018_max = rmnp_summer_2018.max().clip(rmnp_boundary);
var rmnp_summer_2018_min = rmnp_summer_2018.min().clip(rmnp_boundary);
var rmnp_summer_2018_greenest = rmnp_summer_2018.qualityMosaic('NDVI').clip(rmnp_boundary);
print('Median Pixel Composite: ', rmnp_summer_2018_median);
print('Greenest Pixel Composite: ', rmnp_summer_2018_greenest);
```

## Data Postprocessing

```{code-block} javascript
// No data postprocessing in this lab.
```

## Data Visualization

```{code-block} javascript
// Define Sentinel-2 RGB visualization parameters
var s2_vis_params_rgb = {
  'bands': ['B5', 'B3', 'B2'],
  'min': 0,
  'max': 5000
};

// Define NDVI visualization parameters
var vis_params_ndvi = {
  'min': -1,
  'max': 1,
  // palette: ['blue', 'white', 'green']
 'palette': ['red', 'yellow', 'green']
};

// Define RMNP boundary visualization parameters
var empty = ee.Image().byte();

var vt_boundary_vis = empty.paint({
  featureCollection: rmnp_boundary,
  color: 1,
  width: 3
});

// Center map to Rocky Mountain National Park, Colorado
Map.setCenter(-105.6836, 40.3428, 10);

// Add composite images
Map.addLayer(
  rmnp_summer_2018_mean,
  s2_vis_params_rgb,
  'Sentinel 2 - RGB - Summer 2018 - RMNP - Mean', false);

Map.addLayer(
  rmnp_summer_2018_median,
  s2_vis_params_rgb,
  'Sentinel 2 - RGB - Summer 2018 - RMNP - Median', false);

Map.addLayer(
  rmnp_summer_2018_max,
   s2_vis_params_rgb,
  'Sentinel 2 - RGB - Summer 2018 - RMNP - Max', false);

Map.addLayer(
  rmnp_summer_2018_min,
  s2_vis_params_rgb,
  'Sentinel 2 - RGB - Summer 2018 - RMNP - Min', false);

Map.addLayer(
  rmnp_summer_2018_greenest,
  s2_vis_params_rgb,
  'Sentinel 2 - RGB - Summer 2018 - RMNP - Greenest');

Map.addLayer(
  rmnp_summer_2018_greenest.select('NDVI'),
  vis_params_ndvi,
  'Sentinel 2 - NDVI - Summer 2018 - RMNP - Greenest');

// Add RMNP boundary to map
Map.addLayer(
  vt_boundary_vis,
  {'palette': 'FF0000'},
  'RMNP Boundary');
```

## Data Export

```{code-block} javascript
// No data export in this lab.
```

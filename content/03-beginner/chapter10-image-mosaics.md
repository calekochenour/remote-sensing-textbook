# Chapter 10: Image Mosaics

## Data Acquisition & Preprocessing

```{code-block} javascript
// Define boundary for Rocky Mountain National Park, Colorado (from GEE Asset)
var vt_boundary = ee.FeatureCollection("users/calekochenour/vermont_state_boundary");
// print(rmnp_boundary);

// Define Landsat 8 collection
var landsat8_t1_sr = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR');

// Filter Landsat 8
var vermont_summer_median = landsat8_t1_sr
  .filter(ee.Filter.calendarRange(2013, 2020, 'year'))
  .filter(ee.Filter.calendarRange(6, 9, 'month'))
  .filterBounds(vt_boundary)
  .filterMetadata('CLOUD_COVER', 'less_than', 0.45)
  .median().clip(vt_boundary);

print('Vermont Summer Median: ', vermont_summer_median);

// Load and clip the Hansen dataset
var hansen_2015 = ee.Image('UMD/hansen/global_forest_change_2015')
  .clip(vt_boundary);
print('Hansen Dataset: ', hansen_2015);

// Select the mask band
var datamask = hansen_2015.select('datamask');

// Create the binary mask; non-water features, no data (0) and land (1)
// Select water (2) features; water will get value of 1 (used to mask),
//   and no data and land will get values of 0 (don't mask)
var water = datamask.eq(2);
// Map.addLayer(water);

// Create water image (mask water with itself); returns only water objects
//   that had mask values of 1
water = water.mask(water);
// Map.addLayer(water);
```

## Data Processing

```{code-block} javascript
// No data processing in this lab.
```

## Data Postprocessing

```{code-block} javascript
// No data postprocessing in this lab.
```

## Data Visualization

```{code-block} javascript
// Create visualization image for Landsat 8 median composite
var vermont_vis_rgb = vermont_summer_median
  .visualize({
    bands: ['B4', 'B3', 'B2'],
    min: 0,
    max: 2000
});

// Create visualization image for Hansen water mask
var water_vis = water.visualize({
  'palette': 'blue',
  'max': 1,
  'min': 0,
  'opacity': 0.75
});

// Create mosaic from image visualizations
var vermont_mosaic = ee.ImageCollection([vermont_vis_rgb, water_vis]).mosaic();

// Define VT boundary visualization parameters
var empty = ee.Image().byte();

var vt_boundary_vis = empty.paint({
  featureCollection: vt_boundary,
  color: 1,
  width: 3
});

// Center map to Vermont
Map.setCenter(-72.7330, 44.0939, 7);

// Add indiviual visualizations to map
Map.addLayer(vermont_vis_rgb, {}, 'Vermont Median RGB Visualization', false);
Map.addLayer(water_vis, {}, 'Vermont Water Visualization', false);

// Add mosiac to map
Map.addLayer(vermont_mosaic, {}, 'Vermont RGB & Water Mosaic');

// Add RMNP boundary to map
Map.addLayer(
  vt_boundary_vis,
  {'palette': 'FF0000'},
  'Vermont Boundary',
  false);
```

## Data Export

```{code-block} javascript
// No data export in this lab.
```

# Chapter 12: Cloud Masking

## Functions

```{code-block} javascript
/**
 * Mask Landsat 8 image with cloud and shadow masks
 * @param  {ee.image} image - Landsat 8 image
 * @return {ee.Image}       - Masked Landsat 8 image
 */
var mask_clouds_landsat8 = function(image) {
  // Bits 3 and 5 are cloud shadow and cloud, respectively.
  var cloudShadowBitMask = (1 << 3); // 1000 in base 2
  var cloudsBitMask = (1 << 5); // 100000 in base 2

  // Get the pixel QA band.
  var qa = image.select('pixel_qa');

  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa
    .bitwiseAnd(cloudShadowBitMask).eq(0)
    .and(qa.bitwiseAnd(cloudsBitMask).eq(0));

  // Mask image with clouds and shadows
  return image.updateMask(mask);
};

/**
 * Clip image to RMNP boundary
 * @param  {ee.image} image - Image
 * @return {ee.Image}       - Clipped image
 */
var clip_rmnp = function(image) {
  return image.clip(rmnp_boundary);
};
```

## Data Acquisition & Preprocessing

```{code-block} javascript
// Load RMNP boundary from GEE Assets
var rmnp_boundary = ee.FeatureCollection("users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon");

// Get mean of unmasked images for summer 2013-2020
var rmnp_unmasked_mean = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
  .filter(ee.Filter.calendarRange(2013, 2020, 'year'))
  .filter(ee.Filter.calendarRange(6, 9, 'month'))
  .filterBounds(rmnp_boundary)
  .map(clip_rmnp)
  .mean();

// Get mean of masked images for summer 2013-2020
var rmnp_masked_mean = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
  .filter(ee.Filter.calendarRange(2013, 2020, 'year'))
  .filter(ee.Filter.calendarRange(6, 9, 'month'))
  .filterBounds(rmnp_boundary)
  .map(clip_rmnp)
  .map(mask_clouds_landsat8)
  .mean();
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
// Define Landsat 8 RGB visualization parameters
var l8_vis_params_rgb = {
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 3000
};

// Define Landsat 8 CIR visualization parameters
var l8_vis_params_cir = {
  'bands': ['B5', 'B4', 'B3'],
  'min': 0,
  'max': 3000
};

// Center map to Rocky Mountain National Park, Colorado
Map.setCenter(-105.6836, 40.3428, 10);

// Add unmasked and masked composites
Map.addLayer(
  rmnp_unmasked_mean,
  l8_vis_params_rgb,
  'Landsat 8 - RGB - RMNP Unmasked Mean Composite');

Map.addLayer(
  rmnp_masked_mean,
  l8_vis_params_rgb,
  'Landsat 8 - RGB - RMNP Masked Mean Composite');

Map.addLayer(
  rmnp_unmasked_mean,
  l8_vis_params_cir,
  'Landsat 8 - CIR - RMNP Unmasked Mean Composite');

Map.addLayer(
  rmnp_masked_mean,
  l8_vis_params_cir,
  'Landsat 8 - CIR - RMNP Masked Mean Composite');
```

## Data Export

```{code-block} javascript
// No data export in this lab.
```

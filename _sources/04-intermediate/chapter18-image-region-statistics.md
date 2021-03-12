# Chapter 18: Image Region Statistics

Workflow:

* Isolate a single Ecoregion feature for the US High Plains
* Load the USDA NASS Cropland Data Layer, for several years of choosing (available 1997-present)
* Select "cropland" band and clip "cropland" band to the Ecoregion boundary (repeat for all years)
* Select/mask cropland by crop values (e.g. 176 for grassland/pasture) so only the class remains
* Load in Landsat 8, mask clouds/shadow filter on summer, add NDVI band, find mean (each pixel) for summer for each year
* Reduce region to single NDVI mean within the High Plains for each year. Use that as a threshold to predict a future year's grassland/pasture
* Compare prediction grassland to USDA NASS Cropland Data Layer (i.e. show matching, omission, and commission pixels)

[Crop data](https://developers.google.com/earth-engine/datasets/catalog/USDA_NASS_CDL).

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
// Load regions from US Ecoregions Level III
// Southern Rockies (1 feature)
var southern_rockies = ee.Feature(ee.FeatureCollection('EPA/Ecoregions/2013/L3')
  .filter(ee.Filter.eq('us_l3name', 'Southern Rockies'))
  .first());

// High plains (3 features in a collection)
var high_plains_collection = ee.FeatureCollection('EPA/Ecoregions/2013/L3')
  .filter(ee.Filter.eq('us_l3name', 'High Plains'));

// Extract High Plains feature of interest (Northeastern Colorado)
var high_plains_list = high_plains_collection.toList(high_plains_collection.size());
var high_plains = ee.Feature(high_plains_list.get(1));

print('US Ecoregion - Southern Rockies:', southern_rockies);
print('US Ecoregion - High Plains:', high_plains);

// Load USDA NASS Cropland Data Layer for 2014 and 2015
var cropland_2014 = ee.ImageCollection('USDA/NASS/CDL')
  .filter(ee.Filter.date('2014-01-01', '2015-12-31'))
  .first()
  .select('cropland')
  .clip(high_plains);

var cropland_2015 = ee.ImageCollection('USDA/NASS/CDL')
  .filter(ee.Filter.date('2015-01-01', '2016-12-31'))
  .first()
  .select('cropland')
  .clip(high_plains);

print('2014 High Plains Cropland:', cropland_2014);
print('2015 High Plains Cropland:', cropland_2015);

// Select specific crop (grassland/pasture - 176) by masking all other crops to get statistics
var cropland_2014_grassland = cropland_2014.updateMask(cropland_2014.eq(176));
var cropland_2015_grassland = cropland_2015.updateMask(cropland_2015.eq(176));

// Load imagery
// Get Landsat 8 collection with NDVI band, mask clouds and cloud shadows, clip to High Plains
var landsat8_t1_sr = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
  .map(add_ndvi)
  .map(function(image) {
    return image.clip(high_plains)})
  .map(mask_clouds_landsat8);

// Get 2014 Landsat mean composite
var landsat_2014_mean = landsat8_t1_sr
  .filter(ee.Filter.calendarRange(2014, 2014, 'year'))
  .filter(ee.Filter.calendarRange(6, 9, 'month'))
  .mean();

// Mask 2014 Landsat mean composite with grassland pixels
var cropland_2014_mean_grassland = landsat_2014_mean.updateMask(cropland_2014_grassland);

// Get 2015 Landsat mean composite
var landsat_2015_mean = landsat8_t1_sr
  .filter(ee.Filter.calendarRange(2015, 2015, 'year'))
  .filter(ee.Filter.calendarRange(6, 9, 'month'))
  .mean();
```

## Data Processing

```{code-block} javascript
// Reduce grassland pixels to mean value within each band
// Compute individually and on a smaller region (defined in imports)
//   due to GEE timeout with all bands and full region
// Use the 2014 mean values in the smaller region to predict 2015 grassland
var grassland_2014_reduced_mean = cropland_2014_mean_grassland
  .select('NDVI')
  .reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: high_plains_region,
    scale: 30,
    maxPixels: 1e10,
});

/**
 * Mean values for the smaller region (high_plains_region), computed individually
 * NDVI: 0.3940561239815942 (normalized difference vegetation index)
 * B5: 2407.047552441599    (near-infrared)
 * B4: 1042.9063048206513   (red)
 * B3: 922.9315508818664    (green)
 * B2: 616.3030003469779    (blue)
 */

// Define thresholds for masking (based on 2014 data, +/- 5% of mean value)
var ndvi_mean = 0.3940561239815942;
var nir_mean = 2407.047552441599;
var red_mean = 1042.9063048206513;
var green_mean = 922.9315508818664;
var blue_mean = 616.3030003469779;

var threshold_fraction = 0.05;
var threshold_min = 1 - threshold_fraction;
var threshold_max = 1 + threshold_fraction;

var ndvi_min = ndvi_mean * threshold_min;
var ndvi_max = ndvi_mean * threshold_max;
var nir_min = nir_mean * threshold_min;
var nir_max = nir_mean * threshold_max;
var red_min = red_mean * threshold_min;
var red_max = red_mean * threshold_max;
var green_min = green_mean * threshold_min;
var green_max = green_mean * threshold_max;
var blue_min = blue_mean * threshold_min;
var blue_max = blue_mean * threshold_max;

// Predict 2015 grassland based on thresholds - NDVI
var grassland_2015_prediction = landsat_2015_mean.select('NDVI').gt(ndvi_min)
  .and(landsat_2015_mean.select('NDVI').lt(ndvi_max));

// Mask non-grassland pixels in the 2015 prediction
grassland_2015_prediction = grassland_2015_prediction
  .updateMask(grassland_2015_prediction.eq(1));
```

## Data Postprocessing

```{code-block} javascript
// No data postprocessing in this lab.
```

## Data Visualization

```{code-block} javascript
// Landsat 8 RGB visualization parameters
var l8_vis_params_rgb = {
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 3000
};

// NDVI visualization parameters
var vis_params_ndvi = {
  'min': -1,
  'max': 1,
  // palette: ['blue', 'white', 'green']
 'palette': ['red', 'yellow', 'green']
};

// Set map
Map.setCenter(-102.056932, 39.754446, 6);
Map.setOptions('HYBRID');

// RGB - Off by default due to long load time
Map.addLayer(
  landsat_2014_mean, l8_vis_params_rgb,
  'High Plains Cropland - 2014 - NDVI', false);

Map.addLayer(
  landsat_2015_mean, l8_vis_params_rgb,
  'High Plains Cropland - 2015 - NDVI', false);

// NDVI - Off by default due to long load time
Map.addLayer(
  landsat_2014_mean.select('NDVI'), vis_params_ndvi,
  'High Plains Cropland - 2014 - NDVI', false);

Map.addLayer(
  landsat_2015_mean.select('NDVI'), vis_params_ndvi,
  'High Plains Cropland - 2015 - NDVI', false);

// Cropland data
Map.addLayer(cropland_2014, {}, 'High Plains Cropland - 2014');
Map.addLayer(cropland_2015, {}, 'High Plains Cropland - 2015');

// Actual grassland pixels
Map.addLayer(
  cropland_2014_grassland, {},
  'High Plains Cropland - 2014 - Grassland Features');

Map.addLayer(
  cropland_2015_grassland, {},
  'High Plains Cropland - 2015 - Grassland Features - Actual');

// 2015 predicted grassland (based on 2014 data) - Note a long load time
Map.addLayer(
  grassland_2015_prediction, {palette: 'green'},
  'High Plains Cropland - 2015 - Grassland Features - Prediction');

// Ecoregions
var empty = ee.Image().byte();

// For reference, not used in analysis
var southern_rockies_vis = empty.paint({
  featureCollection: southern_rockies,
  color: 1,
  width: 3
});

var high_plains_vis = empty.paint({
  featureCollection: high_plains,
  color: 1,
  width: 3
});

Map.addLayer(southern_rockies_vis, {'palette': 'FF0000'}, 'Ecoregion - Southern Rockies', false);
Map.addLayer(high_plains_vis, {'palette': '00FF00'}, 'Ecoregion - High Plains');
```

## Data Export

```{code-block} javascript
// No data export in this lab.
```

# Chapter 18: Spectral Indices and Math

The full GEE code can be found [here](https://code.earthengine.google.com/ab5068ac521ca53acd3561deb3fd3878).

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

// NDSI  - Snow
var add_ndsi = function(image) {
  var ndsi = image.normalizedDifference(['B3', 'B6']).rename('NDSI');
  return image.addBands(ndsi);
};
```

## Data Acquisition & Preprocessing

```{code-block} javascript
// Define boundary for Rocky Mountain National Park, Colorado (from GEE Asset)
var rmnp_boundary = ee.FeatureCollection("users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon");

// Landsat 8
// Define Landsat 8 collection
var landsat8_t1_sr = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR');

// Filter Landsat 8 Tier 1 SR
var jan_feb = landsat8_t1_sr
  .filterDate('2018-01-01', '2018-02-28')
  .filterBounds(rmnp_boundary)
  .sort('CLOUD_COVER')
  .first()
  .clip(rmnp_boundary);

var mar_apr = landsat8_t1_sr
  .filterDate('2018-03-01', '2018-04-30')
  .filterBounds(rmnp_boundary)
  .sort('CLOUD_COVER')
  .first()
  .clip(rmnp_boundary);

var may_jun = landsat8_t1_sr
  .filterDate('2018-05-01', '2018-06-30')
  .filterBounds(rmnp_boundary)
  .sort('CLOUD_COVER')
  .first()
  .clip(rmnp_boundary);

var jul_aug = landsat8_t1_sr
  .filterDate('2018-07-01', '2018-08-31')
  .filterBounds(rmnp_boundary)
  .sort('CLOUD_COVER')
  .first()
  .clip(rmnp_boundary);

var sep_oct = landsat8_t1_sr
  .filterDate('2018-09-01', '2018-10-31')
  .filterBounds(rmnp_boundary)
  .sort('CLOUD_COVER')
  .first()
  .clip(rmnp_boundary);

var nov_dec = landsat8_t1_sr
  .filterDate('2018-11-01', '2018-12-31')
  .filterBounds(rmnp_boundary)
  .sort('CLOUD_COVER')
  .first()
  .clip(rmnp_boundary);

// Add NDSI band
jan_feb = add_ndsi(jan_feb);
mar_apr = add_ndsi(mar_apr);
may_jun = add_ndsi(may_jun);
jul_aug = add_ndsi(jul_aug);
sep_oct = add_ndsi(sep_oct);
nov_dec = add_ndsi(nov_dec);
```

## Data Processing

```{code-block} javascript
// Compute NDSI difference
var snow_change_1 = mar_apr.select('NDSI').subtract(jan_feb.select('NDSI'));
var snow_change_2 = may_jun.select('NDSI').subtract(mar_apr.select('NDSI'));
var snow_change_3 = jul_aug.select('NDSI').subtract(may_jun.select('NDSI'));
var snow_change_4 = sep_oct.select('NDSI').subtract(jul_aug.select('NDSI'));
var snow_change_5 = nov_dec.select('NDSI').subtract(jul_aug.select('NDSI'));

// Extract snow features based on NDSI > 0.5
var snow_threshold = 0.5;
var jan_feb_snow = jan_feb.updateMask(jan_feb.select('NDSI').gt(snow_threshold));
var mar_apr_snow = mar_apr.updateMask(mar_apr.select('NDSI').gt(snow_threshold));
var may_jun_snow = may_jun.updateMask(may_jun.select('NDSI').gt(snow_threshold));
var jul_aug_snow = jul_aug.updateMask(jul_aug.select('NDSI').gt(snow_threshold));
var sep_oct_snow = sep_oct.updateMask(sep_oct.select('NDSI').gt(snow_threshold));
var nov_dec_snow = nov_dec.updateMask(nov_dec.select('NDSI').gt(snow_threshold));
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

// Define NDSI visualization parameters
var vis_params_ndsi = {
  'min': -1,
  'max': 1,
  palette: ['red', 'green', 'blue', 'white']
  // ['red', 'green', 'blue', 'white']
// 'palette': ['red', 'yellow', 'green']
};

// Define NDSI difference visualization parameters
var vis_params_ndsi_difference = {
  'min': -2,
  'max': 2,
  // palette: ['red', 'green', 'blue', 'white']
  // palette: ['blue', 'white', 'green']
  palette: ['red', 'white', 'green']
};

// Center map to Rocky Mountain National Park, Colorado
Map.setCenter(-105.6836, 40.3428, 10);

// Add RGB images to map
Map.addLayer(jan_feb, l8_vis_params_rgb, 'Jan/Feb', false);
Map.addLayer(mar_apr, l8_vis_params_rgb, 'Mar/Apr', false);
Map.addLayer(may_jun, l8_vis_params_rgb, 'May/Jun');
Map.addLayer(jul_aug, l8_vis_params_rgb, 'Jul/Aug');
Map.addLayer(sep_oct, l8_vis_params_rgb, 'Sep/Oct', false);
Map.addLayer(nov_dec, l8_vis_params_rgb, 'Nov/Dec', false);

// Add NSDI images to map
Map.addLayer(jan_feb.select('NDSI'), vis_params_ndsi, 'NDSI - Jan/Feb', false);
Map.addLayer(mar_apr.select('NDSI'), vis_params_ndsi, 'NDSI - Mar/Apr', false);
Map.addLayer(may_jun.select('NDSI'), vis_params_ndsi, 'NDSI - May/Jun');
Map.addLayer(jul_aug.select('NDSI'), vis_params_ndsi, 'NDSI - Jul/Aug');
Map.addLayer(sep_oct.select('NDSI'), vis_params_ndsi, 'NDSI - Sep/Oct', false);
Map.addLayer(nov_dec.select('NDSI'), vis_params_ndsi, 'NDSI - Nov/Dec', false);

// Add NDSI difference images to map
Map.addLayer(snow_change_1, vis_params_ndsi_difference, 'NDSI change - Jan/Feb to Mar/Apr', false);
Map.addLayer(snow_change_2, vis_params_ndsi_difference, 'NDSI change - Mar/Apr to May/Jun', false);
Map.addLayer(snow_change_3, vis_params_ndsi_difference, 'NDSI change - May/Jun to Jul/Aug');
Map.addLayer(snow_change_4, vis_params_ndsi_difference, 'NDSI change - Jul/Aug to Sep/Oct', false);
Map.addLayer(snow_change_5, vis_params_ndsi_difference, 'NDSI change - Sep/Oct to Nov/Dec', false);

// Add extracted snow features to map
Map.addLayer(jan_feb_snow, l8_vis_params_rgb, 'Jan/Feb Snow', false);
Map.addLayer(mar_apr_snow, l8_vis_params_rgb, 'Mar/Apr Snow', false);
Map.addLayer(may_jun_snow, l8_vis_params_rgb, 'May/Jun Snow', false);
Map.addLayer(jul_aug_snow, l8_vis_params_rgb, 'Jul/Aug Snow', false);
Map.addLayer(sep_oct_snow, l8_vis_params_rgb, 'Sep/Oct Snow', false);
Map.addLayer(nov_dec_snow, l8_vis_params_rgb, 'Nov/Dec Snow', false);
```

## Data Export

```{code-block} javascript
// No data export in this lab.
```

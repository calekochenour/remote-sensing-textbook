# Chapter 7: Qualitative Change Detection

## Background

One of the central values of long-term remote sensing programs is the opportunity to study the changing nature of the land surface. With nearly 9 billion people on the planet, we have a wide array of opportunities to study man-induced change as well as change related to natural land surface processes. The nearly 40-year record of the Landsat program and the growing collections from the National Aeronautics and Space Administration (NASA) Earth Observing System (EOS) Moderate Resolution Imaging Spectroradiometer (MODIS) platform and the European Space Agency (ESA) Sentinel platforms provide great opportunities to discover where long-term change is occurring on Earth's surface.

This chapter introduces a simple, image algebra-based approached to change detection. As in Equation {eq}`equation:1`, one date is subtracted from another and a constant is added in the equation so that you end up with a range of positive values in your difference image.

```{math}
:label: equation:1

change = date_{2} – date_{1} + constant
```

The image histogram for the difference image may then be interpreted to discover where pixels have changes. Those pixels lying closest to the center of the histogram are least likely to have changed, while those in the "tails" of the histogram represent those pixels most likely to have changed between the two image dates. High-resolution imagery, like that found in the GEE Collection of the National Agriculture Imagery Program (NAIP), can be used to aid in the interpretation of the difference image.

## Data Acquisition & Preprocessing

```{code-block} javascript
// Define boundary for Rocky Mountain National Park, Colorado
var rmnp_boundary = ee.FeatureCollection("users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon");

// Define Landsat 8 collection
var landsat8_t1_sr = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR');

// Filter Landsat 8 Tier 1 SR to snow-on conditions near RMNP, 2018
var co_snow_on_2018 = landsat8_t1_sr
  .filterDate('2018-03-01', '2018-04-30')
  .filterBounds(rmnp_boundary)
  .sort('CLOUD_COVER')
  .first();

// Filter Landsat 8 Tier 1 SR to snow-off conditions near RMNP, 2018
var co_snow_off_2018 = landsat8_t1_sr
  .filterDate('2018-07-01', '2018-08-31')
  .filterBounds(rmnp_boundary)
  .sort('CLOUD_COVER')
  .first();

// Clip snow-on and snow-off imagery to RMNP boundary
var rmnp_snow_on_2018 = co_snow_on_2018.clip(rmnp_boundary);
var rmnp_snow_off_2018 = co_snow_off_2018.clip(rmnp_boundary);
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

// Define RMNP boundary visualization parameters
var empty = ee.Image().byte();

var rmnp_boundary_vis = empty.paint({
  featureCollection: rmnp_boundary,
  color: 1,
  width: 3
});

// Center map to Rocky Mountain National Park, Colorado
Map.setCenter(-105.6836, 40.3428, 10);

// Add snow-on and snow-off images to map, RGB and CIR
Map.addLayer(
  rmnp_snow_on_2018,
  l8_vis_params_rgb,
  'Landsat 8 - RGB - 2018 - RMNP - Snow On');

Map.addLayer(
  rmnp_snow_on_2018,
  l8_vis_params_cir,
  'Landsat 8 - CIR - 2018 - RMNP - Snow On');

Map.addLayer(
  rmnp_snow_off_2018,
  l8_vis_params_rgb,
  'Landsat 8 - RGB - 2018 - RMNP - Snow Off');

Map.addLayer(
  rmnp_snow_off_2018,
  l8_vis_params_cir,
  'Landsat 8 - CIR - 2018 - RMNP - Snow Off');

// Add RMNP boundary to map
Map.addLayer(
  rmnp_boundary_vis,
  {'palette': 'FF0000'},
  'RMNP Boundary');
```

## Data Export

```{code-block} javascript
// No data export in this lab.
```

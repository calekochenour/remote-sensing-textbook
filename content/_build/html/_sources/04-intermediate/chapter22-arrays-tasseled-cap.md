# Chapter 22: Arrays and Tasseled Cap

This chapter provides a workflow to explore arrays and the Tasseled Cap transformation for an area near Lake Champlain, Vermont, United States. The full GEE code can be found [here](https://code.earthengine.google.com/997ebbc2046625f80e2b474a6c357617).

## Functions

```{code-block} javascript
/**
 * Creates a Tasseled Cap image for Landsat 5
 * @param   {ee.Image}  image  Landsat 5 image
 * @return  {ee.Image}         Tasseled Cap image with 6 bands:
 *                               'brightness', 'greenness', 'wetness',
 *                               'fourth', 'fifth', sixth'
 */
function tasseled_cap_l5(image) {
  // Define array of Tasseled Cap coefficients
  var coefficients = ee.Array([
    [  0.3037,  0.2793,  0.4743,  0.5585,  0.5082,  0.1863 ],
    [ -0.2848, -0.2435, -0.5436,  0.7243,  0.0840, -0.1800 ],
    [  0.1509,  0.1973,  0.3279,  0.3406, -0.7112, -0.4572 ],
    [ -0.8242,  0.0849,  0.4392, -0.0580,  0.2012, -0.2768 ],
    [ -0.3280,  0.0549,  0.1075,  0.1855, -0.4357,  0.8085 ],
    [  0.1084, -0.9022,  0.4120,  0.0573, -0.0251,  0.0238 ]
  ]);

  // Select bands for use in Tasseled Cap
  var image_bands_tc = image.select(['B1', 'B2', 'B3', 'B4', 'B5', 'B7']);

  // Create 1-D array image (vector of length 6 for all bands per pixel)
  var array_image_1d = image_bands_tc.toArray();

  // Create 2-D array image (6x1 matrix for all bands per pixel) from 1-D array
  var array_image_2d = array_image_1d.toArray(1);

  // Get a multi-band image with TC-named bands
  // Matrix multiplication: 6x6 times 6x1
  var components_image = ee.Image(coefficients)
    .matrixMultiply(array_image_2d)
    // Remove extra dimensions
    .arrayProject([0])
    // Convert to regular image
    .arrayFlatten([['brightness', 'greenness', 'wetness', 'fourth', 'fifth', 'sixth']]);

  return components_image;
}
```

## Data Acquisition & Preprocessing
```{code-block} javascript
// Set geometries
var lake_champlain =
    /* color: #d63000 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Feature(
        ee.Geometry.Polygon(
            [[[-74.72224061263952, 45.50738144646654],
              [-74.72224061263952, 43.32625155252435],
              [-71.89875428451452, 43.32625155252435],
              [-71.89875428451452, 45.50738144646654]]], null, false),
        {
          "system:index": "0"
        });
```

```{code-block} javascript
// Get Landsat 5 T1 TOA
var landsat5_t1_toa = ee.ImageCollection("LANDSAT/LT05/C01/T1_TOA");

// Get median image for Lake Champlain, VT area
var lake_champlain_august = landsat5_t1_toa
  .filterBounds(lake_champlain.geometry())
  .filter(ee.Filter.calendarRange(1984, 2012, 'year'))
  .filter(ee.Filter.calendarRange(8, 8, 'month'))
  .filterMetadata('CLOUD_COVER', 'less_than', 0.25)
  .mean()
  .clip(lake_champlain);

var lake_champlain_october = landsat5_t1_toa
  .filterBounds(lake_champlain.geometry())
  .filter(ee.Filter.calendarRange(1984, 2012, 'year'))
  .filter(ee.Filter.calendarRange(10, 10, 'month'))
  .filterMetadata('CLOUD_COVER', 'less_than', 0.25)
  .median()
  .clip(lake_champlain);

print('Lake Champlain August Mean:', lake_champlain_august);
print('Lake Champlain October Mean:', lake_champlain_october);
```

## Data Processing

```{code-block} javascript
var lake_champlain_august_tc = tasseled_cap_l5(lake_champlain_august);
var lake_champlain_october_tc = tasseled_cap_l5(lake_champlain_october);
print('Lake Champlain August Tasseled Cap:', lake_champlain_august_tc);
print('Lake Champlain Octobber Tasseled Cap:', lake_champlain_october_tc);
```

## Data Postprocessing

```{code-block} javascript
// No data postprocessing in this lab.
```

## Data Visualization

```{code-block} javascript
// Center map on Lake Champlain, VT
Map.setCenter(-73.3801, 44.5866, 7);

// Define visualization parameters
var vis_params_rgb = {
  min: 0,
  max: 0.2,
  bands: ['B3', 'B2', 'B1']
};

var vis_params_tc = {
  min: -0.1,
  max: [0.5, 0.1, 0.1],
  bands: ['brightness', 'greenness', 'wetness']
};

var vis_params_tc_brightness = {
  min: -0.1,
  max: 0.5,
  bands: ['brightness'],
  palette: [
    'ffffcc',
    'ffeda0',
    'fed976',
    'feb24c',
    'fd8d3c',
    'fc4e2a',
    'e31a1c',
    'bd0026',
    '800026'
  ]
};

var vis_params_tc_greenness = {
  min: -0.1,
  max: 0.25,
  bands: ['greenness'],
  palette: [
    'ffffe5',
    'f7fcb9',
    'd9f0a3',
    'addd8e',
    '78c679',
    '41ab5d',
    '238443',
    '006837',
    '004529'
  ]
};

var vis_params_tc_wetness = {
  min: -0.1,
  max: 0.1,
  bands: ['wetness'],
  palette: [
    'fff7fb',
    'ece7f2',
    'd0d1e6',
    'a6bddb',
    '74a9cf',
    '3690c0',
    '0570b0',
    '045a8d',
    '023858'
  ]
};

// Add RGB images
Map.addLayer(lake_champlain_august, vis_params_rgb, 'August Mean - RGB');
Map.addLayer(lake_champlain_october, vis_params_rgb, 'October Mean - RGB');

// Add Tasseled Cap images - all bands (Brightness, Greenness, Wetness)
Map.addLayer(lake_champlain_august_tc, vis_params_tc, 'August - Tasseled Cap - All');
Map.addLayer(lake_champlain_october_tc, vis_params_tc, 'October - Tasseled Cap - All');

// Add Tasseled Cap images - individual bands
Map.addLayer(lake_champlain_august_tc, vis_params_tc_brightness, 'August - Tasseled Cap - Brightness');
Map.addLayer(lake_champlain_august_tc, vis_params_tc_greenness, 'August - Tasseled Cap - Greenness');
Map.addLayer(lake_champlain_august_tc, vis_params_tc_wetness, 'August - Tasseled Cap - Wetness');
Map.addLayer(lake_champlain_october_tc, vis_params_tc_brightness, 'October - Tasseled Cap - Brightness');
Map.addLayer(lake_champlain_october_tc, vis_params_tc_greenness, 'October - Tasseled Cap - Greenness');
Map.addLayer(lake_champlain_october_tc, vis_params_tc_wetness, 'October - Tasseled Cap - Wetness');
```

## Data Export

```{code-block} javascript
// No data export in this lab.
```

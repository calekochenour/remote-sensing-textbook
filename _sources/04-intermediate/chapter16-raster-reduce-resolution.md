# Chapter 16: Raster Reduce Resolution

## Functions

```{code-block} javascript
// Add NDVI band to image for NAIP
function add_ndvi_naip(image) {
  return image.addBands(image.normalizedDifference(['N', 'R']).rename('NDVI'));
}

// Add NDVI band to image for Landsat 8
function add_ndvi_landsat8(image) {
  return image.addBands(image.normalizedDifference(['B5', 'B4']).rename('NDVI'));
}
```

## Data Acquisition & Preprocessing

```{code-block} javascript
// Define location for Equinox Pond in Manchester, Vermont
var equinox_pond = ee.Geometry.Point([-73.08971970400783, 43.15588067987059]);

// Get a single NAIP image near Manchester, Vermont
var vt_naip = ee.ImageCollection("USDA/NAIP/DOQQ")
  .filterBounds(equinox_pond)
  .filterDate('2018-01-01', '2020-12-31')
  .first();

print('NAIP:', vt_naip);  
print('NAIP Spatial Extent:', vt_naip.geometry());

// Get landsat image and clip to NAIP extent
var vt_landsat8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
  .filter(ee.Filter.calendarRange(2018, 2018, 'year'))
  .filter(ee.Filter.calendarRange(10, 10, 'month'))
  .filterBounds(equinox_pond)
  .sort('CLOUD_COVER')
  .first()
  .clip(vt_naip.geometry());

print('Landsat 8:', vt_landsat8);

// Add NDVI bands
var vt_naip_ndvi = add_ndvi_naip(vt_naip);
var vt_landsat8_ndvi = add_ndvi_landsat8(vt_landsat8);
print('NAIP with NDVI Band:', vt_naip_ndvi);
print('Landsat 8 with NDVI Band:', vt_landsat8_ndvi);

// Display scale (spatial resolution, GSD)
print('NAIP Resolution (meters):', vt_naip_ndvi.projection().nominalScale());
print('Landsat 8 Resolution (meters):', vt_landsat8_ndvi.projection().nominalScale());

// Get the NAIP image at the Landsat 8 scale and projection
var vt_naip_rescale = vt_naip_ndvi
  .reduceResolution({reducer: ee.Reducer.mean(), maxPixels: 4096})
  .reproject({crs: vt_landsat8_ndvi.projection()});
// print('NAIP - Rescaled:', vt_naip_rescale);

// Compute difference between Landsat 8 NDVI and rescaled NAIP NDVI
var ndvi_difference = vt_landsat8_ndvi.select('NDVI')
  .subtract(vt_naip_rescale.select('NDVI'))
  .select(['NDVI'], ['ndvi_diff']);
print('NDVI Difference:', ndvi_difference);
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
// Set map options for viewing
// NOTE: Setting the zoom level to less than 15 will cause the program to take too much time processing and cause an error.
Map.centerObject(equinox_pond, 15);

// Define visualization parameters
var vis_params_rgb_naip = {
  'bands': ['R', 'G', 'B']
};

var vis_params_rgb_landsat8 = {
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 1000
};

var vis_params_ndvi = {
  'min': -1,
  'max': 1,
  'palette': ['blue', 'white', 'green']
};

var vis_params_ndvi_diff = {
  'min': -2,
  'max': 2,
  'palette': [
    '#0571b0',
    '#92c5de',
    '#f7f7f7',
    '#f4a582',
    '#ca0020'
  ]
};

// Add NAIP images to map
Map.addLayer(vt_naip, vis_params_rgb_naip, 'VT NAIP - RGB');
Map.addLayer(vt_naip_ndvi.select('NDVI'), vis_params_ndvi, 'VT NAIP - NDVI');
Map.addLayer(vt_naip_rescale.select('NDVI'), vis_params_ndvi, 'VT NAIP - NDVI - Rescale');

// Add Landsat 8 images to map
Map.addLayer(vt_landsat8, vis_params_rgb_landsat8, 'VT Landsat 8 - RGB');
Map.addLayer(vt_landsat8_ndvi.select('NDVI'), vis_params_ndvi, 'VT Landsat 8 - NDVI');

// Add NDVI difference to map
Map.addLayer(ndvi_difference, vis_params_ndvi_diff, 'NDVI Difference (Landsat8 - NAIP)');
```

## Data Export

```{code-block} javascript
// No data export in this lab.
```

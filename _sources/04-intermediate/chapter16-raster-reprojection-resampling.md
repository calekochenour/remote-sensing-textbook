# Chapter 16: Raster Reprojection and Resampling

This chapter provides a workflow to reproject and resample imagery for an area near Equinox Mountain, Manchester, Vermont. The full GEE code can be found [here](https://code.earthengine.google.com/d759f759e511223324d6f4b9879807d9).

GEE resources for [projections](https://developers.google.com/earth-engine/guides/projections) and [scale](https://developers.google.com/earth-engine/guides/scale).

## Functions

```{code-block} javascript
// Add NDVI band to image for NAIP
function add_ndvi(image) {
  return image.addBands(image.normalizedDifference(['N', 'R']).rename('NDVI'));
}
```

## Data Acquisition & Preprocessing

```{code-block} javascript
// Define location for Equinox Pond in Manchester, Vermont
var equinox_pond = ee.Geometry.Point([-73.08971970400783, 43.15588067987059]);

// Check map scale at different zoom levels
Map.centerObject(equinox_pond, 0);
print('Map Scale (meters) at Zoom Level 0:', Map.getScale());  
Map.centerObject(equinox_pond, 4);
print('Map Scale (meters) at Zoom Level 4:', Map.getScale());  
Map.centerObject(equinox_pond, 8);
print('Map Scale (meters) at Zoom Level 8:', Map.getScale());  
Map.centerObject(equinox_pond, 12);
print('Map Scale (meters) at Zoom Level 12:', Map.getScale());  
Map.centerObject(equinox_pond, 16);
print('Map Scale (meters) at Zoom Level 16:', Map.getScale());  
Map.centerObject(equinox_pond, 20);
print('Map Scale (meters) at Zoom Level 20:', Map.getScale());  
Map.centerObject(equinox_pond, 24);
print('Map Scale (meters) at Zoom Level 24:', Map.getScale());

// Get a single NAIP image near Manchester, Vermont
var vt_naip = ee.ImageCollection("USDA/NAIP/DOQQ")
  .filterBounds(equinox_pond)
  .filterDate('2018-01-01', '2020-12-31')
  .first();

// Check image info, projection info, and scale for VT NAIP image
print('VT NAIP:', vt_naip);
print('VT NAIP Projection, CRS, and CRS Transform:', vt_naip.projection());
print('VT NAIP Scale (meters):', vt_naip.projection().nominalScale());

// Resample image with bilinear and bicubic
var vt_naip_bl = vt_naip.resample('bilinear');
var vt_naip_bc = vt_naip.resample('bicubic');

// Add NDVI band and resample
var ndvi_nn = add_ndvi(vt_naip).select('NDVI');
var ndvi_bl = add_ndvi(vt_naip).select('NDVI').resample('bilinear');
var ndvi_bc = add_ndvi(vt_naip).select('NDVI').resample('bicubic');

// Add NDVI band, resample, and reproject
var ndvi_nn_rp = add_ndvi(vt_naip).select('NDVI')
  .reproject(vt_naip.projection(), null, vt_naip.projection().nominalScale());
var ndvi_bl_rp = add_ndvi(vt_naip).select('NDVI')
  .reproject(vt_naip.projection(), null, vt_naip.projection().nominalScale())
  .resample('bilinear');
var ndvi_bc_rp = add_ndvi(vt_naip).select('NDVI')
  .reproject(vt_naip.projection(), null, vt_naip.projection().nominalScale())
  .resample('bicubic');
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
Map.centerObject(equinox_pond, 12);

// Define visualization parameters
var vis_params_rgb_naip = {
  bands: ['R', 'G', 'B']
};

var vis_params_ndvi = {
  min: -1,
  max: 1,
  palette: ['blue', 'white', 'green']
};

// Add NAIP RGB images to map
Map.addLayer(vt_naip, vis_params_rgb_naip, 'VT NAIP - Nearest Neighbor Resampling');
Map.addLayer(vt_naip_bl, vis_params_rgb_naip, 'VT NAIP - Bilinear Resampling');
Map.addLayer(vt_naip_bc, vis_params_rgb_naip, 'VT NAIP - Bicubic Resampling');

// Add NDVI resampled
Map.addLayer(ndvi_nn, vis_params_ndvi, 'NDVI - NN');
Map.addLayer(ndvi_bl, vis_params_ndvi, 'NDVI - BL');
Map.addLayer(ndvi_bc, vis_params_ndvi, 'NDVI - BC');

// Add NDVI resampled and reprojected
Map.addLayer(ndvi_nn_rp, vis_params_ndvi, 'NDVI - NN - RP');
Map.addLayer(ndvi_bl_rp, vis_params_ndvi, 'NDVI - BL - RP');
Map.addLayer(ndvi_bc_rp, vis_params_ndvi, 'NDVI - BC - RP');
```

## Data Export

```{code-block} javascript
// No data export in this lab.
```

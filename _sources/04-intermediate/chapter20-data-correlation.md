# Chapter 20: Data Correlation

## Functions

```{code-block} javascript
/**
 * Calculates and adds the NDVI band for Sentinel-2A
 */
function add_ndvi_s2(image) {
  return image.addBands(image.normalizedDifference(['B8', 'B4']).rename('NDVI'));
}

/**
 * Clips an image to the Gabilan Range, CA study area
 */
function clip_gabilan(image) {
  return image.clip(gabilan_range);
}
```
## Data Acquisition & Preprocessing

```{code-block} javascript
// Define geometries
var gabilan_range =
    /* color: #5eff32 */
    /* shown: false */
    ee.Feature(
        ee.Geometry.Polygon(
            [[[-121.39209915128892, 36.41211982460723],
              [-121.40445877042954, 36.4270383353476],
              [-121.42780471769517, 36.43753482852815],
              [-121.43261123624985, 36.445820531007755],
              [-121.44977737394517, 36.45797129413855],
              [-121.48136306730454, 36.47785025501275],
              [-121.48960281339829, 36.4872357700071],
              [-121.51157546964829, 36.50489953730563],
              [-121.52256179777329, 36.52311107716474],
              [-121.53904128996079, 36.534698007435544],
              [-121.54728103605454, 36.55621198679144],
              [-121.57955337492173, 36.5733085705686],
              [-121.60907913175767, 36.59205531122498],
              [-121.6660707089061, 36.620717990097226],
              [-121.6825502010936, 36.62457561415858],
              [-121.69628311124985, 36.60252944801643],
              [-121.71962905851548, 36.58102836805629],
              [-121.75464797941392, 36.56999984966293],
              [-121.75602127042954, 36.554557277884626],
              [-121.75052810636704, 36.53690484497294],
              [-121.75602127042954, 36.526421805784025],
              [-121.75533462492173, 36.500483973199884],
              [-121.7484681698436, 36.49330814444738],
              [-121.71894241300767, 36.475641733322036],
              [-121.71070266691392, 36.46238928152319],
              [-121.68844847586017, 36.449460428394225],
              [-121.6458764543758, 36.44227987424441],
              [-121.61909727957111, 36.425154332654465],
              [-121.56828551199298, 36.39199739069815],
              [-121.57377867605548, 36.382600351332194],
              [-121.5634789934383, 36.37928347804693],
              [-121.53875975515705, 36.3411292687819],
              [-121.52777342703205, 36.337257506937185],
              [-121.5085473528133, 36.34278853636809],
              [-121.49962096121173, 36.3322792446237],
              [-121.48451476003986, 36.31346960497832],
              [-121.44194273855548, 36.26864011750132],
              [-121.42408995535236, 36.257013453780026],
              [-121.40211729910236, 36.270854523880075],
              [-121.36366515066486, 36.26587202121934],
              [-121.34993224050861, 36.27030092817272],
              [-121.33413939382892, 36.27030092817272],
              [-121.32246642019611, 36.28081857542688],
              [-121.30942015554767, 36.31291631156002],
              [-121.33345274832111, 36.39531372165556]]]),
        {
          "system:index": "0"
        }),

var test_region =
    /* color: #ff371b */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-121.52367515823046, 36.43004814282859],
          [-121.52367515823046, 36.36372428812449],
          [-121.42342491408984, 36.36372428812449],
          [-121.42342491408984, 36.43004814282859]]], null, false);
```

```{code-block} javascript
// Get USGS National Elevation Dataset
var usgs_ned = ee.Image("USGS/NED");

// Clip elevation data to Gabilan Range, CA and create slope and aspect layers
var gabilan_range_elevation = usgs_ned.clip(gabilan_range);
var gabilan_range_slope = ee.Terrain.slope(gabilan_range_elevation);
var gabilan_range_aspect = ee.Terrain.aspect(gabilan_range_elevation);

print('Elevation:', gabilan_range_elevation);
print('Slope:', gabilan_range_slope);
print('Aspect:', gabilan_range_aspect);

// Get Sentinel-2A collection
var sentinel_2a = ee.ImageCollection("COPERNICUS/S2_SR");

// Get monthly median composites
var jun_2019 = sentinel_2a
  .filterBounds(gabilan_range.geometry())
  .filter(ee.Filter.date('2019-06-01', '2019-06-30'))
  .map(clip_gabilan)
  .map(add_ndvi_s2)
  .median();

var jul_2019 = sentinel_2a
  .filterBounds(gabilan_range.geometry())
  .filter(ee.Filter.date('2019-07-01', '2019-07-31'))
  .map(clip_gabilan)
  .map(add_ndvi_s2)
  .median();

var aug_2019 = sentinel_2a
  .filterBounds(gabilan_range.geometry())
  .filter(ee.Filter.date('2019-08-01', '2019-08-31'))
  .map(clip_gabilan)
  .map(add_ndvi_s2)
  .median();

var sep_2019 = sentinel_2a
  .filterBounds(gabilan_range.geometry())
  .filter(ee.Filter.date('2019-09-01', '2019-09-30'))
  .map(clip_gabilan)
  .map(add_ndvi_s2)
  .median();

var oct_2019 = sentinel_2a
  .filterBounds(gabilan_range.geometry())
  .filter(ee.Filter.date('2019-10-01', '2019-10-31'))
  .map(clip_gabilan)
  .map(add_ndvi_s2)
  .median();

var nov_2019 = sentinel_2a
  .filterBounds(gabilan_range.geometry())
  .filter(ee.Filter.date('2019-11-01', '2019-11-30'))
  .map(clip_gabilan)
  .map(add_ndvi_s2)
  .median();
```

## Data Processing

```{code-block} javascript
// Create image for correlation analysis (single image with necesssary bands)
// Clip to area smaller than full study area so that the elevation and NDVI
//  layers have the same number of pixels (otherwise array shapes won't match,
//  causing the charts to fail)
var correlation_base = ee.Image([
  gabilan_range_aspect.select('aspect'),
  gabilan_range_slope.select('slope'),
  gabilan_range_elevation.select('elevation'),
  jun_2019.select('NDVI').rename('ndvi_jun'),
  jul_2019.select('NDVI').rename('ndvi_jul'),
  aug_2019.select('NDVI').rename('ndvi_aug'),
  sep_2019.select('NDVI').rename('ndvi_sep'),
  oct_2019.select('NDVI').rename('ndvi_oct'),
  nov_2019.select('NDVI').rename('ndvi_nov')
]).clip(test_region);
print('Correlation Image Base:', correlation_base);

// Reduce image to dictionary; band names as keys, pixel values in lists
var pixel_lists = correlation_base.reduceRegion(
  ee.Reducer.toList(),
  test_region,
  30 // Scaled to 30 for computation time       -->  90,000 elements per band
     // Using scale of 10 (Sentinel resolution) --> 820,000 elements per band
);
print('Pixel Lists:', pixel_lists);
```

## Data Postprocessing

```{code-block} javascript
// No data postprocessing in this lab.
```

## Data Visualization

```{code-block} javascript
// Set map
Map.setCenter(-121.563559, 36.461750, 10);
Map.setOptions('TERRAIN');

// Define Sentinel-2 RGB visualization parameters
var vis_params_s2_rgb = {
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 2500
};

// Define NDVI visualization parameters
var vis_params_ndvi = {
  'min': -1,
  'max': 1,
  palette: ['blue', 'white', 'green']
// 'palette': ['red', 'yellow', 'green']
};

// Add terrain layers to map
Map.addLayer(
  gabilan_range_elevation,
  {
    min: 0.0,
    max: 1250.0,
    palette: [
      'blue',
      'green',
      'yellow',
      'orange',
      'red',
      'brown',
      'white'
    ]
  },
  'Elevation'
);


Map.addLayer(
  gabilan_range_slope,
  {
    min: 0.0,
    max: 60, // 90 is max
    palette: ['green', 'yellow', 'orange', 'red']
  },
  'Slope'
);

Map.addLayer(
  gabilan_range_aspect,
  {
    min: 0.0,
    max: 360,
    palette: [
      '#666666',
      '#bf5b17',
      '#f0027f',
      '#386cb0',
      '#ffff99',
      '#fdc086',
      '#beaed4',
      '#7fc97f'
    ]
  },
  'Aspect'
);

// Add image layers to map
Map.addLayer(jun_2019, vis_params_s2_rgb, 'June 2019 Median RGB');
Map.addLayer(jul_2019, vis_params_s2_rgb, 'July 2019 Median RGB');
Map.addLayer(aug_2019, vis_params_s2_rgb, 'August 2019 Median RGB');
Map.addLayer(sep_2019, vis_params_s2_rgb, 'September 2019 Median RGB');
Map.addLayer(oct_2019, vis_params_s2_rgb, 'October 2019 Median RGB');
Map.addLayer(nov_2019, vis_params_s2_rgb, 'November 2019 Median RGB');

// Add NDVI layers to map
Map.addLayer(jun_2019.select('NDVI'), vis_params_ndvi, 'June 2019 Median NDVI');
Map.addLayer(jul_2019.select('NDVI'), vis_params_ndvi, 'July 2019 Median NDVI');
Map.addLayer(aug_2019.select('NDVI'), vis_params_ndvi, 'August 2019 Median NDVI');
Map.addLayer(sep_2019.select('NDVI'), vis_params_ndvi, 'September 2019 Median NDVI');
Map.addLayer(oct_2019.select('NDVI'), vis_params_ndvi, 'October 2019 Median NDVI');
Map.addLayer(nov_2019.select('NDVI'), vis_params_ndvi, 'November 2019 Median NDVI');

// Select variables for plotting correlation
// Dependent (terrain)
var x_values_elevation = pixel_lists.get('elevation');
var x_values_slope = pixel_lists.get('slope');
var x_values_aspect = pixel_lists.get('aspect');

// Independent (NDVI)
var y_values_jun = ee.Array(pixel_lists.get('ndvi_jun'));
var y_values_jul = ee.Array(pixel_lists.get('ndvi_jul'));
var y_values_aug = ee.Array(pixel_lists.get('ndvi_aug'));
var y_values_sep = ee.Array(pixel_lists.get('ndvi_sep'));
var y_values_oct = ee.Array(pixel_lists.get('ndvi_oct'));
var y_values_nov = ee.Array(pixel_lists.get('ndvi_nov'));

// Create correlation charts (commented out due to display/processing time)
// Elevation
// var chart_ndvi_jun_elevation = ui.Chart.array.values(y_values_jun, 0, x_values_elevation)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Elevation - June 2019',
//     hAxis: {'title': 'Elevation (meters)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_jul_elevation = ui.Chart.array.values(y_values_jul, 0, x_values_elevation)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Elevation - July 2019',
//     hAxis: {'title': 'Elevation (meters)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_aug_elevation = ui.Chart.array.values(y_values_aug, 0, x_values_elevation)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Elevation - August 2019',
//     hAxis: {'title': 'Elevation (meters)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_sep_elevation = ui.Chart.array.values(y_values_sep, 0, x_values_elevation)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Elevation - September 2019',
//     hAxis: {'title': 'Elevation (meters)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_oct_elevation = ui.Chart.array.values(y_values_oct, 0, x_values_elevation)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Elevation - October 2019',
//     hAxis: {'title': 'Elevation (meters)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_nov_elevation = ui.Chart.array.values(y_values_nov, 0, x_values_elevation)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Elevation - November 2019',
//     hAxis: {'title': 'Elevation (meters)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// Slope
// var chart_ndvi_jun_slope = ui.Chart.array.values(y_values_jun, 0, x_values_slope)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Slope - June 2019',
//     hAxis: {'title': 'Slope (degrees)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_jul_slope = ui.Chart.array.values(y_values_jul, 0, x_values_slope)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Slope - July 2019',
//     hAxis: {'title': 'Slope (degrees)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_aug_slope = ui.Chart.array.values(y_values_aug, 0, x_values_slope)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Slope - August 2019',
//     hAxis: {'title': 'Slope (degrees)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_sep_slope = ui.Chart.array.values(y_values_sep, 0, x_values_slope)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Slope - September 2019',
//     hAxis: {'title': 'Slope (degrees)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_oct_slope = ui.Chart.array.values(y_values_oct, 0, x_values_slope)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Slope - October 2019',
//     hAxis: {'title': 'Slope (degrees)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_nov_slope = ui.Chart.array.values(y_values_nov, 0, x_values_slope)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Slope - November 2019',
//     hAxis: {'title': 'Slope (degrees)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// Aspect
// var chart_ndvi_jun_aspect = ui.Chart.array.values(y_values_jun, 0, x_values_aspect)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Aspect - June 2019',
//     hAxis: {'title': 'Aspect (degrees)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_jul_aspect = ui.Chart.array.values(y_values_jul, 0, x_values_aspect)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Aspect - July 2019',
//     hAxis: {'title': 'Aspect (degrees)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_aug_aspect = ui.Chart.array.values(y_values_aug, 0, x_values_aspect)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Aspect - August 2019',
//     hAxis: {'title': 'Aspect (degrees)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_sep_aspect = ui.Chart.array.values(y_values_sep, 0, x_values_aspect)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Aspect - September 2019',
//     hAxis: {'title': 'Aspect (degrees)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_oct_aspect = ui.Chart.array.values(y_values_oct, 0, x_values_aspect)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Aspect - October 2019',
//     hAxis: {'title': 'Aspect (degrees)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// var chart_ndvi_nov_aspect = ui.Chart.array.values(y_values_nov, 0, x_values_aspect)
//   .setSeriesNames(['NDVI'])
//   .setOptions({
//     title: 'Sentinel-2A Median NDVI vs. NED Aspect - November 2019',
//     hAxis: {'title': 'Aspect (degrees)'},
//     vAxis: {'title': 'NDVI'},
//     pointSize: 3,
// });

// Display correlation charts (commented out due to display/processing time)
// Elevation
// print(chart_ndvi_jun_elevation);
// print(chart_ndvi_jul_elevation);
// print(chart_ndvi_aug_elevation);
// print(chart_ndvi_sep_elevation);
// print(chart_ndvi_oct_elevation);
// print(chart_ndvi_nov_elevation);

// Slope
// print(chart_ndvi_jun_slope);
// print(chart_ndvi_jul_slope);
// print(chart_ndvi_aug_slope);
// print(chart_ndvi_sep_slope);
// print(chart_ndvi_oct_slope);
// print(chart_ndvi_nov_slope);

// Aspect
// print(chart_ndvi_jun_aspect);
// print(chart_ndvi_jul_aspect);
// print(chart_ndvi_aug_aspect);
// print(chart_ndvi_sep_aspect);
// print(chart_ndvi_oct_aspect);
// print(chart_ndvi_nov_aspect);
```

## Data Export

```{code-block} javascript
// No data export in this lab.
```

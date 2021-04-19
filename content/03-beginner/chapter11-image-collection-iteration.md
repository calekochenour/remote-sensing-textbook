# Chapter 11: Image Collection Iteration

This chapter provides a workflow to iterate through an image collection and calculate the cumulative NDVI difference for imagery in Rocky Mountain National Park, Colorado, United States. The full GEE code can be found [here](https://code.earthengine.google.com/1ee1873e73c10cf12223c94260428b0f).

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

/**
 * Mask Landsat 8 image with cloud and shadow masks
 * @param  {ee.Image} image - Landsat 8 image
 * @param  {ee.List}  list  - List with initialize image
 * @return {ee.Image}       - Masked Landsat 8 image
 */
var accumulate = function(image, list) {
  // Get the latest cumulative anomaly image from the end of the list with
  // get(-1).  Since the type of the list argument to the function is unknown,
  // it needs to be cast to a List. Since the return type of get() is unknown,
  // cast it to Image
  var previous = ee.Image(ee.List(list).get(-1));
  // Add the current anomaly to make a new cumulative anomaly image
  var added = image.add(previous)
    // Propagate metadata to the new image
    .set('system:time_start', image.get('system:time_start'));
  // Return the list with the cumulative anomaly inserted
  return ee.List(list).add(added);
};
```

## Data Acquisition & Preprocessing

```{code-block} javascript
// Define boundary for Rocky Mountain National Park, Colorado (from GEE Asset)
var rmnp_boundary = ee.FeatureCollection("users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon");
// print(rmnp_boundary);

// Define Landsat 8 collection
var landsat8_t1_sr = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR');

// Add NDVI band to each image in the collection (with mapping)
var landsat8_t1_sr_ndvi = landsat8_t1_sr.map(add_ndvi).select('NDVI');

// Filter Landsat 8 NDVI collection for June-September for 2013-2018 (baseline/reference data)
var rmnp_summer_ndvi = landsat8_t1_sr_ndvi
  .filter(ee.Filter.calendarRange(2013, 2018, 'year'))
  .filter(ee.Filter.calendarRange(6, 9, 'month'))
  .filterBounds(rmnp_boundary)
  .sort('system:time_start', false);
print(rmnp_summer_ndvi, 'NDVI');
```

## Data Processing

```{code-block} javascript
// Compute mean for the entire NDVI collection; clip to RMNP
var rmnp_summer_ndvi_mean = rmnp_summer_ndvi.mean().clip(rmnp_boundary);

// Compute NDVI difference (image - reference mean) series for all images post-baseline (2019-2020)
var rmnp_ndvi_diff_series = landsat8_t1_sr_ndvi
  .filter(ee.Filter.calendarRange(2019, 2020, 'year'))
  .filter(ee.Filter.calendarRange(6, 9, 'month'))
  .filterBounds(rmnp_boundary)
  .map(function(image) {
    return image.clip(rmnp_boundary)})
  .map(function(image) {
    return image.subtract(rmnp_summer_ndvi_mean).set('system:time_start', image.get('system:time_start'));
});
print(rmnp_ndvi_diff_series, "NDVI Difference Series (collection)");

// Compute min and max accumulated NDVI difference (for plotting min/max)
var ndvi_diff_min = ee.Number(rmnp_ndvi_diff_series.sum().reduceRegion({
  reducer: ee.Reducer.min(),
  geometry: rmnp_boundary.geometry(),
  scale: 30,
  maxPixels: 1e9
}).get('NDVI'));

var ndvi_diff_max = ee.Number(rmnp_ndvi_diff_series.sum().reduceRegion({
  reducer: ee.Reducer.max(),
  geometry: rmnp_boundary.geometry(),
  scale: 30,
  maxPixels: 1e9
}).get('NDVI'));

// Print min/max to the Console
print('Accumulated NDVI Difference Min: ', ndvi_diff_min);
print('Accumulated NDVI Difference Max: ', ndvi_diff_max);

// Type of object
print('Type: ', ndvi_diff_min.name());

// Get the timestamp from the most recent image in the reference collection
var time_0 = rmnp_summer_ndvi.first().get('system:time_start');
print('Time Zero: ', time_0);

// Initialize difference (anomaly) accumulation to 0 (image with all 0s and timestamp time_0)
var initialized_accumulation = ee.List([
  // Rename the first band from 'constant' (default) to 'NDVI'
  ee.Image(0).set('system:time_start', time_0).select([0], ['NDVI']).clip(rmnp_boundary)
]); // This is a list
print('Initialzed accumulation: ', initialized_accumulation);
print('Type: ', initialized_accumulation.name());

// Create an ImageCollection of cumulative anomaly images (NDVI differences)
// Cast return object of .iterate() to type List, as it is by default unknown (ComputedObject)
var ndvi_diff_cumulative = ee.ImageCollection(
  // .iterate() takes a function as param 1 and the initial state as param 2
  ee.List(rmnp_ndvi_diff_series.iterate(accumulate, initialized_accumulation))
);
print('Accumulated collection via iteration: ', ndvi_diff_cumulative);
print('Accumulated collection via iteration type: ', ndvi_diff_cumulative.name());
```

## Data Postprocessing

```{code-block} javascript
// No data postprocessing in this lab.
```

## Data Visualization

```{code-block} javascript
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

// Add layers to map
Map.addLayer(
  rmnp_summer_ndvi_mean,
   vis_params_ndvi,
  'Landsat 8 - NDVI Mean - Jun/Sep 2013/2020');

  // Display accumulated NDVI differences (anomalies from 6-year mean)
Map.addLayer(
  rmnp_ndvi_diff_series.sum(),
  {
    min: -2.5899382242647437,
    max: 2.548139614675886,
    palette: ['FF0000', '000000', '00FF00']
  },
  'Cumulative NDVI Difference'
);

// Add RMNP boundary to map
Map.addLayer(
  vt_boundary_vis,
  {'palette': 'FF0000'},
  'RMNP Boundary');

// Define chart titles
var chart_titles = {
  title: 'Cumulative NDVI Difference Over Time',
  hAxis: {title: 'Time'},
  vAxis: {title: 'Cumulative NDVI Difference'},
};

// Define test points (pixels) for charting
var ute_trail_west_tree = ee.Geometry.Point([-105.77114730224609, 40.44397929249563]);
var ute_trail_west_rock = ee.Geometry.Point([-105.76848655090332, 40.43672831058668]);
var ute_trail_east_tree = ee.Geometry.Point([-105.6988694765701, 40.39268322603617]);
var ute_trail_east_rock = ee.Geometry.Point([-105.69552207971951, 40.3929447073708]);

// Add charts to Console
print('Ute Trail West - Trees',
  ui.Chart.image.series(
    ndvi_diff_cumulative,
    ute_trail_west_tree,
    ee.Reducer.first(),
    500)
  .setOptions(chart_titles)
);

print('Ute Trail West - Rocks',
  ui.Chart.image.series(
    ndvi_diff_cumulative,
    ute_trail_west_rock,
    ee.Reducer.first(),
    500)
  .setOptions(chart_titles)
);

print('Ute Trail East - Trees',
  ui.Chart.image.series(
    ndvi_diff_cumulative,
    ute_trail_east_tree,
    ee.Reducer.first(),
    500)
  .setOptions(chart_titles)
);

print('Ute Trail East - Rocks',
  ui.Chart.image.series(
    ndvi_diff_cumulative,
    ute_trail_east_rock,
    ee.Reducer.first(),
    500)
  .setOptions(chart_titles)
);
```

## Data Export

```{code-block} javascript
// No data export in this lab.
```

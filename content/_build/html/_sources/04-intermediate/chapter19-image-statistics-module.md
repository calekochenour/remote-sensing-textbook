# Chapter 19: Image Statistics Module

## Functions

```{code-block} javascript
/**
 * Get single statistic (mean, median, min, max)
 * @param  {ee.Image}                          image       Image to compute statistic for
 * @param  {ee.FeatureCollection or Geometry}  region      Area to compute statistic for
 * @param  {string}                            statistic   Statistic for calculation (mean, median, min, max)
 * @param  {int}                               scale       Image scale
 * @param  {int}                               max_pixels  Maximum number of pixels
 * @return {object}                                        Object/dictionary with statistic for all bands
 */
function get_statistic(image, region, statistic, scale, max_pixels) {
  // Ensure region is of type Geometry
  if (region.name() != 'Geometry') {
    region = region.geometry();
  }

  // Get correct reducer (mean if invalid value specified)
  if (statistic.toLowerCase() == "mean") {
    statistic = ee.Reducer.mean();
  } else if (statistic.toLowerCase() == "median") {
    statistic = ee.Reducer.median();
  } else if (statistic.toLowerCase() == "min") {
    statistic = ee.Reducer.min();
  } else if (statistic.toLowerCase() == "max") {
    statistic = ee.Reducer.max();
  } else {
    statistic = ee.Reducer.mean();
  }

  // Compute and return statistic
  return image.reduceRegion({
    reducer: statistic,
    geometry: region,
    scale: scale,
    maxPixels: max_pixels});
}

/**
 * Get several statistics (mean, median, min, max)
 * @param  {ee.Image}                          image       Image to compute statistics for
 * @param  {ee.FeatureCollection or Geometry}  region      Area to compute statistics for
 * @param  {int}                               scale       Image scale
 * @param  {int}                               max_pixels  Maximum number of pixels
 * @return {object}                                        Object/dictionary with all statistics for all bands
 */
function get_statistics(image, region, scale, max_pixels) {
  // Ensure region is of type Geometry
  if (region.name() != 'Geometry') {
    region = region.geometry();
  }

  // Compute mean
  var mean = image.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: region,
    scale: scale,
    maxPixels: max_pixels});

  // Compute median
  var median = image.reduceRegion({
    reducer: ee.Reducer.median(),
    geometry: region,
    scale: scale,
    maxPixels: max_pixels});

  // Compute minimum
  var min = image.reduceRegion({
    reducer: ee.Reducer.min(),
    geometry: region,
    scale: scale,
    maxPixels: max_pixels});

  // Compute maximum
  var max = image.reduceRegion({
    reducer: ee.Reducer.max(),
    geometry: region,
    scale: scale,
    maxPixels: max_pixels});

  // Centralize statistics
  statistics = ee.Dictionary({
    'mean': mean,
    'median': median,
    'min': min,
    'max': max
  });

  return statistics;
}
```

## Data Acquisition & Preprocessing
```{code-block} javascript
// Get boundary for RMNP, CO
var rmnp_boundary = ee.FeatureCollection("users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon");

// Get 2018 least cloudy image for RMNP, CO
var rmnp =  ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
  .filterBounds(rmnp_boundary)
  .filterDate('2018-01-01', '2018-12-31')
  .sort('CLOUD_COVER')// Use for single year
  .first()
  .clip(rmnp_boundary);

// print(rmnp);
```

## Data Processing
```{code-block} javascript
// Compute mean individually
var mean = get_statistic(rmnp, rmnp_boundary, 'mean', 30, 1e12);
print('Mean:', mean);

// Get single band value and cast to type ee.Number
print('Mean B1:', ee.Number(mean.get('B1')));

// Compute all statistics (mean, median, min, max)
var statistics = get_statistics(rmnp, rmnp_boundary, 30, 1e12);
print('All:', statistics);

// Get max dictionary and single band from max
print('Max:', statistics.get('max'));
print('Max B1:', ee.Dictionary(statistics.get('max')).get('B1'));
```

## Data Postprocessing

```{code-block} javascript
// No data postprocessing in this lab.
```

## Data Visualization

```{code-block} javascript
// Add image to map
var vis_params_landsat8_rgb = {
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 3000
};

// Center map to Rocky Mountain National Park, Colorado
Map.setCenter(-105.6836, 40.3428, 10);
Map.addLayer(rmnp, vis_params_landsat8_rgb, "RMNP");
```

## Data Export

```{code-block} javascript
// No data export in this lab.
```

# Chapter 26: Alpine Treeline in Colorado

Partial implementation of "Spatial Detection of Alpine Treeline Ecotones in the Western United States" (Wei, Karger, and Wilson, 2020), applied to Rocky Mountain National Park, Colorado.

Reference:

* [DOI](https://doi.org/10.1016/j.rse.2020.111672)

## Functions

```{code-block} javascript
/**
 * Calculates and adds the NDVI band for Sentinel-2A
 * @param   {ee.Image}  image  - Sentinel-2A image
 * @return  {ee.Image}         - Sentinel-2A image with NDVI band added
 */
function add_ndvi_s2(image) {
  return image.addBands(image.normalizedDifference(['B8', 'B4']).rename('NDVI'));
}

/**
 * Calculates and adds the NDVI band for Landsat 8
 * @param   {ee.Image}  image  - Landsat 8 image
 * @return  {ee.Image}         - Landsat 8 image with NDVI band added
 */
function add_ndvi_l8(image) {
  return image.addBands(image.normalizedDifference(['B5', 'B4']).rename('NDVI'));
}

/**
 * Clips an image to the RMNP, CO boundary
 * @param   {ee.Image}  image  - Full-sized image
 * @return  {ee.Image}         - Image clipped to RMNP boundary
 */
function clip_rmnp(image) {
  return image.clip(rmnp_boundary);
}

/**
 * Extracts QA values from an image
 * @param  {ee.Image} qa_band   - Single-band image of the QA layer
 * @param  {Integer}  start_bit - Starting bit
 * @param  {Integer}  end_bit   - Ending bit
 * @param  {String}   band_name - param_description
 * @return {ee.Image}           - Image with extracted QA values
 */
function extract_qa_bits(qa_band, start_bit, end_bit, band_name) {
  // Initialize QA bit string/pattern to check QA band against
  var qa_bits = 0;
  // Add each specified QA bit flag value/string/pattern to the QA bits to check/extract
  for (var bit = start_bit; bit <= end_bit; bit++) {
    qa_bits += Math.pow(2, bit); // Same as qa_bits += (1 << bit);
  }
  // Return a single band image of the extracted QA bit values
  return qa_band
    // Rename output band to specified name
    .select([0], [band_name])
    // Check QA band against specified QA bits to see what QA flag values are set
    .bitwiseAnd(qa_bits)
    // Get value that matches bitmask documentation
    // (0 or 1 for single bit,  0-3 or 0-N for multiple bits)
    .rightShift(start_bit);
}

/**
 * Masks clouds, cloud shadows, water, and snow pixles in a Landsat 8 image
 * @param   {ee.Image}  qa_band  - Unmasked image
 * @return  {ee.Image}           - Masked image
 */
function mask_landsat8(image) {
  // Select pixel QA band
  var qa_band = image.select('pixel_qa');

  // Extract bitmasks for water (bit 2), cloud shadow (bit 3), snow (bit 4), and cloud (bit 5)
  var water_bitmask = extract_qa_bits(qa_band, 2, 2, 'water_bitmask');
  var cloud_shadow_bitmask = extract_qa_bits(qa_band, 3, 3, 'cloud_shadow_bitmask');
  var snow_bitmask = extract_qa_bits(qa_band, 4, 4, 'snow_bitmask');
  var cloud_bitmask = extract_qa_bits(qa_band, 5, 5, 'cloud_bitmask');

  // Mask image
  var image_masked = image.updateMask(
    water_bitmask.eq(0)
    .and(cloud_shadow_bitmask.eq(0))
    .and(snow_bitmask.eq(0))
    .and(cloud_bitmask.eq(0))
  );

  return image_masked;
}

/**
 * Creates a standard score image
 * @param   {ee.Image}              image       Image
 * @param   {ee.FeatureCollection}  study_area  Area to capture statistics for
 * @param   {string}                band_name   Band within the image to return
 * @return  {ee.Image}                          Standard score image of the specified band
 */
function standardize_component(image, study_area, band_name) {
  // Calculate mean
  var mean = ee.Number(image.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: study_area.geometry(),
    scale: 30,
    maxPixels: 1e12
  }).get(band_name));

  // Calculate standard deviation
  var stdev = ee.Number(image.reduceRegion({
    reducer: ee.Reducer.stdDev(),
    geometry: study_area.geometry(),
    scale: 30,
    maxPixels: 1e12
  }).get(band_name));

  // Calculate standard score image
  var standardized = image
    .subtract(mean)
    .divide(stdev)
    .select([band_name], [band_name + '_standardized']);

  return standardized;
}

/**
 * Export image/raster as GeoTiff to Google Drive or to GEE Asset
 * @param   {ee.Image}              image           Image/raster that will be exported
 * @param   {ee.FeatureCollection}  study_area      Study area boundary
 * @param   {ee.Number}             max_pixels      Maximum number of pixels to reduce
 * @param   {ee.Number}             raster_scale    Scale in meters
 * @param   {string}                output_name     Name of the output file (without extension)
 * @param   {string}                output_method   Name of the export method/location ("Drive" for Google Drive, "Asset" for GEE Asset)
 * @return  {string}                output_message  Message indicating the task to run to complete the export
 */
function export_raster(raster, study_area, raster_scale, max_pixels, output_name, output_method) {
  // Handle optional parameters
  output_method = output_method || 'drive';
  raster_scale = raster_scale || 30;
  max_pixels = max_pixels || 1e7;

  // Create variable for output message
  var output_message;

  if (output_method.toLowerCase() == "drive") {

    // Export image/raster as a GeoTiff to Google Drive
    Export.image.toDrive({
      image: raster,
      region: study_area,
      scale: raster_scale,
      maxPixels: max_pixels,
      description: output_name
    });

    // Assign output message
    output_message = "Task ready: " + output_name + "\nPlease run task to export to Google Drive.";

  } else if (output_method.toLowerCase() == "asset") {

    // Export vector to GEE Asset
    Export.image.toAsset({
      image: raster,
      geometry: study_area,
      scale: raster_scale,
      maxPixels: max_pixels,
      description: output_name,
      assetId: output_name
    });

    // Assign output message
    output_message = "Task ready: " + output_name + "\nPlease run task to export to GEE Asset.";

  } else {

    // Assign output message
    output_message = "Invalid export method. Please specify 'Drive' or 'Asset'.";

  }

  // Return output message
  return output_message;
}
```

## Data Acquisition & Preprocessing

```{code-block} javascript
/** Pseudocode
 * Study Area
 *   Upload study area shapefile to EE asset
 *   Get study area boundary into feature collection
 *
 * Imagery
 *   Get a year's worth of imagery into a collection
 *   Add NDVI band to each band in the collection
 *   Clip collection to study area boundary
 *   Mask collection for clouds, cloud shadows, snow, and water
 *   Select NDVI band; create max NDVI composite
 *   Apply focal median (300 meter / 10 pixel radius) to smooth NDVI
 *
 * Elevation
 *   Get elevation layer
 *   Clip to study area boundary
 *   Apply focal median (300 meter / 10 pixel radius to smooth NDVI
 */

// STUDY AREA
// Rocky Mountain National Park, Colorado (from GEE Asset)
var rmnp_boundary = ee.FeatureCollection("users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon");
// print('RMNP Bounadry:', rmnp_boundary);

// IMAGERY
// Landsat 8
var landsat8_t1_sr = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR");

// Get 2018 imagery for RMNP
var rmnp_2018_collection = landsat8_t1_sr
  .filterBounds(rmnp_boundary)
  .filterDate('2018-01-01', '2018-12-31') // Use for single year
  // .filter(ee.Filter.calendarRange(2013, 2020, 'year')) // Use for multi-year
  // .filter(ee.Filter.calendarRange(6, 9, 'month')) // Use for multi-year
  .map(clip_rmnp)
  .map(add_ndvi_l8)
  .map(mask_landsat8);
// print(rmnp_2018_collection);

// Create greenest pixel composite (max NDVI)
var rmnp_2018_greenest = rmnp_2018_collection.qualityMosaic('NDVI');
print('Greenest Pixel:', rmnp_2018_greenest);

// Define kernal for smoothing NDVI and elevation
var ate_kernel = ee.Kernel.circle({radius: 10, units: 'pixels'});

// Smooth NDVI with focal median
var ndvi_greenest = rmnp_2018_greenest.select('NDVI');
var ndvi_greenest_smoothed = ndvi_greenest
  .focal_median({kernel: ate_kernel, iterations: 1})
  .clip(rmnp_boundary);

print('NDVI Greenest (Max):', ndvi_greenest);
print('NDVI Greenest (Max) Smoothed:', ndvi_greenest_smoothed);

// ELEVATION
// Get USGS National Elevation Dataset elevation layer
var usgs_ned = ee.Image("USGS/NED");
var rmnp_elevation = usgs_ned.clip(rmnp_boundary);
var rmnp_elevation_smoothed = rmnp_elevation
  .focal_median({kernel: ate_kernel, iterations: 1})
  .clip(rmnp_boundary);

print('Elevation:', rmnp_elevation);
print('Elevation Smoothed:', rmnp_elevation_smoothed);
```

## Data Processing

```{code-block} javascript
// C1 - Abrupt spatial shift in NDVI / spatial velocity of NDVI
// Compute gradient of smoothed NDVI
var ndvi_gradient = ndvi_greenest_smoothed.gradient();
print('NDVI Gradient:', ndvi_gradient);

// Compute NDVI gradient magnitude
var ndvi_gradient_magnitude = ndvi_gradient
  .select('x').pow(2).add(ndvi_gradient
  .select('y').pow(2)).sqrt().select(['x'], ['ndvi_grad_mag']);
print('NDVI Gradient Magnitude:', ndvi_gradient_magnitude);

// Get min/max for plotting gradient magnitude
// var ndvi_gradient_magnitude_max = ndvi_gradient_magnitude.reduceRegion({
//   reducer: ee.Reducer.max(),
//   geometry: rmnp_boundary.geometry(),
//   scale: 30,
//   maxPixels: 1e12
// });
// print('NDVI Gradient Magnitude Max:', ndvi_gradient_magnitude_max); // 0.005956791228225612

// var ndvi_gradient_magnitude_min = ndvi_gradient_magnitude.reduceRegion({
//   reducer: ee.Reducer.min(),
//   geometry: rmnp_boundary.geometry(),
//   scale: 30,
//   maxPixels: 1e12
// });
// print('NDVI Gradient Magnitude Min:', ndvi_gradient_magnitude_min); // 0

// Compute NDVI gradient direction (degrees) (from north, + --> clockwise, - --> counterclockwise)
var ndvi_gradient_direction = ndvi_gradient
  .select('y').atan2(ndvi_gradient
  .select('x'))
  .multiply(180).divide(Math.PI)
  // Ensure positive angles (0 = North, 90 = East, 180 = South, 270 = West)
  .add(360).mod(360)
  .select(['y'], ['ndvi_grad_dir']);
// Gradient vector: direction and rate of fastest increase
// Direction in most cases should be down the mountain (at least when in ATE)
print('NDVI Gradient Direction:', ndvi_gradient_direction);

// Get C1 component
var c1 = ndvi_gradient_magnitude.select(['ndvi_grad_mag'], ['c1']);
print('C1 Component:', c1);

// C2 - Intermediate NDVI
// Define parameters (based on paper, can change with calibration)
var b = 0.44;
var c = 0.06;

// Compute C2 (Gaussian function of NDVI)
var c2 = ee.Image(Math.E).clip(rmnp_boundary)
  .pow(ndvi_greenest_smoothed.subtract(b).pow(2)
  .divide(ee.Number(c).pow(2).multiply(ee.Number(2))).multiply(-1))
  .select(['constant'], ['c2']);
print('C2 Component:', c2);

// C3 - Spatial covariation of NDVI and elevation
// Compute gradient of smoothed elevation
var elevation_gradient = rmnp_elevation_smoothed.gradient();
print('Elevation Gradient:', elevation_gradient);

// Compute elevation gradient magnitude
var elevation_gradient_magnitude = elevation_gradient
  .select('x').pow(2).add(elevation_gradient
  .select('y').pow(2)).sqrt().select(['x'], ['elevation_grad_mag']);
print('Elevation Gradient Magnitude:', elevation_gradient_magnitude);

// Get min/max values for plotting
// var elevation_gradient_magnitude_min = elevation_gradient_magnitude.reduceRegion({
//   reducer: ee.Reducer.min(),
//   geometry: rmnp_boundary.geometry(),
//   scale: 30,
//   maxPixels: 1e12
// });
// print('Elevation Gradient Magnitude Min:', elevation_gradient_magnitude_min); // 0

// var elevation_gradient_magnitude_max = elevation_gradient_magnitude.reduceRegion({
//   reducer: ee.Reducer.max(),
//   geometry: rmnp_boundary.geometry(),
//   scale: 30,
//   maxPixels: 1e12
// });
// print('Elevation Gradient Magnitude Max:', elevation_gradient_magnitude_max); // 3.137629831784505

// Compute elevation gradient direction (degrees) (from north, + --> clockwise, - --> counterclockwise)
var elevation_gradient_direction = elevation_gradient
  .select('y').atan2(elevation_gradient
  .select('x'))
  .multiply(180).divide(Math.PI)
  // Ensure positive angles (0 = North, 90 = East, 180 = South, 270 = West)
  .add(360).mod(360)
  .select(['y'], ['elevation_grad_dir']);
// Gradient vector: direction and rate of fastest increase
// Direction in most cases should be down the mountain (at least when in ATE)
print('Elevation Gradient Direction:', elevation_gradient_direction);

// Compute difference between NDVI elevation gradient directions
var theta = ndvi_gradient_direction
  .subtract(elevation_gradient_direction)
  // Ensure positive angles (0-360) for difference
  // 90 < theta < 270 --> opposite directions
  // theta < 90 or theta > 270 --> same direction
  .add(360).mod(360);

// Define C3 parameters
var n = 10; // Based on paper value

// Compute C3
var c3 = theta.cos().multiply(-1).add(1).pow(n)
  .divide(ee.Number(2).pow(n))
  .select(['ndvi_grad_dir'], ['c3']);
print('C3 Component:', c3);

// Standardize ATE components
var c1_standardized = standardize_component(c1, rmnp_boundary, 'c1');
var c2_standardized = standardize_component(c2, rmnp_boundary, 'c2');
var c3_standardized = standardize_component(c3, rmnp_boundary, 'c3');

print('C1 Standardized:', c1_standardized);
print('C2 Standardized:', c2_standardized);
print('C3 Standardized:', c3_standardized);

// Calculate Alpine Treeline Ecotone Index (ATEI)

// ATEI = e^x/(e^x+1)
// x --> b0 + b1*c1 + b2*c2 + b3*c3
// Use values from paper
var b0 = -1.47;
// print(b0);
var b1 = 0.44;
var b2 = 0.58;
var b3 = 0.56;

// Compute sum component of ATEI equation
var atei_sum = c1_standardized.multiply(b1)
  .add(c2_standardized.multiply(b2))
  .add(c3_standardized.multiply(b3))
  .add(b0)
  .select(['c1_standardized'], ['atei_sum_comp']);
print('ATEI Sum Component Image:', atei_sum);

// Compute exponent component of ATEI equation
var atei_exponent = ee.Image(Math.E).clip(rmnp_boundary).pow(atei_sum)
  .select(['constant'], ['atei_exp_comp']);
print('ATEI Exponent Component Image:', atei_exponent);

// Compute full ATEI
var atei = atei_exponent.divide(atei_exponent.add(1))
  .select(['atei_exp_comp'], ['atei']);
print('ATEI Image:', atei);

// Get min/max values for plotting
var atei_min = atei.reduceRegion({
  reducer: ee.Reducer.min(),
  geometry: rmnp_boundary.geometry(),
  scale: 30,
  maxPixels: 1e12
});
print('ATEI Min:', atei_min);

var atei_max = atei.reduceRegion({
  reducer: ee.Reducer.max(),
  geometry: rmnp_boundary.geometry(),
  scale: 30,
  maxPixels: 1e12
});
print('ATEI Max:', atei_max);
```

## Data Postprocessing

```{code-block} javascript
// Smooth ATEI image (prepare for export)
var atei_kernel = ee.Kernel.circle({radius: 3, units: 'pixels'});
var atei_smoothed = atei
  .focal_median({kernel: atei_kernel, iterations: 1})
  .clip(rmnp_boundary);
```

## Data Visualization

```{code-block} javascript
// VISUALIZATION PARAMETERS
// Landsat 8 RGB
var vis_params_landsat8_rgb = {
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 3000
};

// NDVI
var vis_params_ndvi = {
  bands: ['NDVI'],
  'min': -1,
  'max': 1,
  palette: ['ffffff', 'f7fcb9', 'addd8e', '31a354']
};

var vis_params_elevation_rmnp = {
  min: 2000.0,
  max: 5000.0,
  palette: [
    'blue',
    'green',
    'yellow',
    'orange',
    'red',
    'brown',
    'white'
  ]
};

var vis_params_gradient_direction = {
  min: 0,
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
};

// Center map to Rocky Mountain National Park, Colorado
Map.setCenter(-105.6836, 40.3428, 10);

// ADD LAYERS TO MAP
// RGB
Map.addLayer(rmnp_2018_greenest, vis_params_landsat8_rgb, 'RMNP - 2018 - Greenest Pixel - RGB');

// NDVI
// Map.addLayer(rmnp_2018_greenest, vis_params_ndvi, 'RMNP, CO - 2018 - Greenest Pixel Composite - NDVI');
Map.addLayer(ndvi_greenest, vis_params_ndvi, 'RMNP - 2018 - Greenest Pixel - NDVI');
Map.addLayer(ndvi_greenest_smoothed, vis_params_ndvi, 'RMNP - 2018 - Greenest Pixel - NDVI Smoothed');

// Elevation
Map.addLayer(rmnp_elevation, vis_params_elevation_rmnp, 'RMNP - Elevation');
Map.addLayer(rmnp_elevation_smoothed, vis_params_elevation_rmnp, 'RMNP - Elevation Smoothed');

// NDVI gradient
Map.addLayer(ndvi_gradient, {}, 'NDVI Gradient');
Map.addLayer(
  ndvi_gradient_magnitude,
  {
    min: 0,
    max: 0.005956791228225612,
    // palette: [
    //   '0571b0',
    //   'f7f7f7',
    //   'ca0020'
    // ]
    palette: [
      '404040',
      'bababa',
      'ffffff',
      'f4a582',
      'ca0020'
    ]
  },
  'NDVI Gradient Magnitude');
Map.addLayer(
  ndvi_gradient_direction,
  vis_params_gradient_direction,
  'NDVI Gradient Direction'
);

// Elevation gradient
Map.addLayer(elevation_gradient, {}, 'Elevation Gradient');
Map.addLayer(
  elevation_gradient_magnitude,
  {
    min: 0,
    max: 3.137629831784505,
    // palette: [
    //   '0571b0',
    //   'f7f7f7',
    //   'ca0020'
    // ]
    palette: [
      '404040',
      'bababa',
      'ffffff',
      'f4a582',
      'ca0020'
    ]
  },
  'Elevation Gradient Magnitude');
Map.addLayer(
  elevation_gradient_direction,
  vis_params_gradient_direction,
  'Elevation Gradient Direction'
);

// Gradient difference
Map.addLayer(
  theta,
  {
    min: 0,
    max: 360,
    palette: [
      '0571b0', // Same direction - 0-90
      'ca0020', // Different direction - 90-180
      'ca0020', // Different direction - 180-270
      '0571b0'  // Same direction - 270-360
    ]
  },
  "Difference in Gradient Direction"
);

// Alpine treeline ecotone components
Map.addLayer(c1, {min: 0, max: 0.005956791228225612}, 'C1 Component');
// Map.addLayer(c2, {}, 'C2 Component');
Map.addLayer(
  c2,
  {min: 0, max: 1},
  // {min: 0, max: 1000, palette: ['blue', 'white', 'red']},
  'C2 Component');
Map.addLayer(c3, {}, 'C3 Component');

Map.addLayer(
  c1_standardized,
  {
    palette: [
      '0571b0',
      '92c5de',
      'f7f7f7',
      'f4a582',
      'ca0020'
    ]
  },
  'C1 Standardized');

Map.addLayer(
  c2_standardized,
  {
    palette: [
      '0571b0',
      '92c5de',
      'f7f7f7',
      'f4a582',
      'ca0020'
    ]
  },
  'C2 Standardized');

Map.addLayer(
  c3_standardized,
  {
    palette: [
      // '0571b0',
      // '92c5de',
      // 'f7f7f7',
      // 'f4a582',
      // 'ca0020'
      'fef0d9',
      'fdcc8a',
      'fc8d59',
      'e34a33',
      'b30000'
    ]
  },
  'C3 Standardized');

// ATEI
Map.addLayer(
  atei,
  {
    min: 0,
    max: 1,
    palette: [
      'fff7f3',
      'fde0dd',
      'fcc5c0',
      'fa9fb5',
      'f768a1',
      'dd3497',
      'ae017e',
      '7a0177',
      '49006a'  
    ]
  },
  'Alpine Treeline Ecotone Index'
);

// ATEI - smoothed
Map.addLayer(
  atei_smoothed,
  {
    min: 0,
    max: 1,
    palette: [
      'fff7f3',
      'fde0dd',
      'fcc5c0',
      'fa9fb5',
      'f768a1',
      'dd3497',
      'ae017e',
      '7a0177',
      '49006a'  
    ]
  },
  'Alpine Treeline Ecotone Index - Smoothed - 3 Pixel Circular Median Kernel'
);
```

## Data Export

```{code-block} javascript
// Export ATEI raster
var atei_export = export_raster(
  atei,
  rmnp_boundary,
  undefined, // use default value defined in function
  1e8,
  'atei_rmnp_co_2018'
);

print(atei_export);

// Export smoothed ATEI raster
var atei_smoothed_export = export_raster(
  atei_smoothed,
  rmnp_boundary,
  undefined, // use default value defined in function
  1e8,
  'atei_smoothed_rmnp_co_2018'
);

print(atei_smoothed_export);
```

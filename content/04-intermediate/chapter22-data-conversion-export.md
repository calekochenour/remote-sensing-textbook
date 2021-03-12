# Chapter 22: Data Conversion and Export

## Functions

```{code-block} javascript
/**
 * Calculate and add NDSI (snow) band to Landsat 8 image
 * @param  {ee.Image} image - Landsat 8 image
 * @return {ee.Image}       - Landsat 8 image with NDSI band added
 */
function add_ndsi(image) {
  return image.addBands(image.normalizedDifference(['B3', 'B6']).rename('NDSI'));
}

/**
 * Convert raster to vector
 * @param  {ee.Image}              raster        Primary or secondary rice field candidates
 * @param  {ee.FeatureCollection}  study_area    Study area boundary
 * @param  {ee.Number}             max_pixels    Maximum number of pixels to reduce
 * @param  {ee.Number}             raster_scale  Scale in meters
 * @return {ee.FeatureCollection}                Rice fields coverted to vector feature
 */
function raster_to_vector(raster, study_area, max_pixels, raster_scale) {
  // Handle optional parameters
  max_pixels = max_pixels || 1e7;
  raster_scale = raster_scale || 30;

  // Convert raster to vector
  return raster.reduceToVectors({
    geometry: study_area,
    maxPixels: max_pixels,
    scale: raster_scale
  });
}

/**
 * Export vector as shapefile to Google Drive or to GEE Asset
 * @param   {ee.FeatureCollection}  vector          Vector that will be exported
 * @param   {string}                output_name     Name of the output file (without extension)
 * @param   {string}                output_method   Name of the export method/location ("Drive" for Google Drive, "Asset" for GEE Asset)
 * @return  {string}                output_message  Message indicating the task to run to complete the export
 */
function export_vector(vector, output_name, output_method) {
  // Handle optional parameters
  output_method = output_method || 'drive';

  // Create variable for output message
  var output_message;

  if (output_method.toLowerCase() == "drive") {

    // Export vectors a shapefile to Google Drive
    Export.table.toDrive({
      collection: vector,
      description: output_name,
      fileFormat: 'SHP'
    });

    // Assign output message
    output_message = "Task ready: " + output_name + "\nPlease run task to export to Google Drive.";

  } else if (output_method.toLowerCase() == "asset") {

    // Export vector to GEE Asset
    Export.table.toAsset({
      collection: vector,
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

// Add NDSI band
jan_feb = add_ndsi(jan_feb);
```

## Data Processing

```{code-block} javascript
// Extract snow features based on NDSI > 0.5
var jan_feb_snow = jan_feb.select('NDSI').gt(0.5);
var jan_feb_snow_raster = jan_feb_snow.updateMask(jan_feb_snow.eq(1));

// Convert to vector (prepare for export)
var jan_feb_snow_vector = raster_to_vector(jan_feb_snow_raster, rmnp_boundary, 1e8);
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


// Define NDSI visualization parameters
var vis_params_ndsi = {
  'min': -1,
  'max': 1,
  palette: ['red', 'green', 'blue', 'white']
};

// Center map to Rocky Mountain National Park, Colorado
Map.setCenter(-105.6836, 40.3428, 10);

// Add RGB image to map
Map.addLayer(jan_feb, l8_vis_params_rgb, 'RMNP - Jan/Feb 2019 - RGB');

// Add NSDI image to map
Map.addLayer(jan_feb.select('NDSI'), vis_params_ndsi, 'RMNP - Jan/Feb 2019 - NDSI');

// Add extracted snow features to map
// Raster
Map.addLayer(jan_feb_snow_raster, {}, 'RMNP - Jan/Feb 2019 - Snow - Raster');

// Vector
Map.addLayer(jan_feb_snow_vector, {color: 'white'}, 'RMNP - Jan/Feb 2019 - Snow - Vector');
```

## Data Export

```{code-block} javascript
// Export snow features
// Raster
var raster_export = export_raster(
  jan_feb_snow_raster,
  rmnp_boundary,
  undefined, // use default value defined in function
  1e8,
  'rmnp_snow_jan_feb_raster'
);

// Vector
var vector_export = export_vector(jan_feb_snow_vector, 'rmnp_snow_jan_feb_vector');

// Display export messages
print(raster_export);
print(vector_export);
```

# Chapter 25: Agricultural Field Edge Detection

This chapter provides a partial implementation of Watkins and van Niekerk {cite}`WATKINS2019294` to delineate agriculture field boundaries in the Vaalharts Irrigation Scheme, South Africa. The full GEE code can be found [here](https://code.earthengine.google.com/a7bc95e9d2dcc0fd9f5695fd075d4068).

## Functions

```{code-block} javascript
/**
 * Create and aggregate Canny Edge layers for Red, Green, Blue, and Near-Infrared
 * @param  {ee.Image}      image      Sentinel-2 Level-1C image
 * @param  {int or float}  threshold  Value for edge detection magnitude
 * @param  {int or float}  sigma      Value for gaussian filter applied before edge detection
 * @return {ee.Image}                 Aggregate Canny Edges for R/G/B/NIR
 */
function aggregate_canny_edges(image, threshold, sigma) {
  // Get Canny edge for Red, Green, Blue, and NIR
  var canny_red = ee.Algorithms.CannyEdgeDetector({
    image: image.select('B4'), threshold: threshold, sigma: sigma
  });

  var canny_green = ee.Algorithms.CannyEdgeDetector({
    image: image.select('B3'), threshold: threshold, sigma: sigma
  });

  var canny_blue = ee.Algorithms.CannyEdgeDetector({
    image: image.select('B2'), threshold: threshold, sigma: sigma
  });

  var canny_nir = ee.Algorithms.CannyEdgeDetector({
    image: image.select('B8'), threshold: threshold, sigma: sigma
  });

  // Aggregate R/G/B/NIR Canny edges
  var canny_aggregate = canny_red.add(canny_green).add(canny_blue).add(canny_nir)
    .select(['B4'], ['canny_rgbn']);

  return canny_aggregate;
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
// Set geometries
var vaalharts_irrigation_scheme =
    /* color: #d63000 */
    /* shown: false */
    ee.Geometry.Polygon(
        [[[24.65986591490829, -28.09412322046305],
          [24.70106464537704, -28.054136830234732],
          [24.754622994986416, -28.032319800398245],
          [24.78071552428329, -28.03110761344614],
          [24.790328561392666, -28.004436046690174],
          [24.82466083678329, -27.9862471006372],
          [24.87135273131454, -27.941367915030856],
          [24.883712350455166, -27.90982002972256],
          [24.86860614928329, -27.866123149358096],
          [24.850753366080166, -27.811477263231893],
          [24.83564716490829, -27.7798915448951],
          [24.817794381705166, -27.750727353214696],
          [24.806808053580166, -27.710613834239876],
          [24.798568307486416, -27.674134193214723],
          [24.79719501647079, -27.637642367457204],
          [24.78346210631454, -27.62547571967499],
          [24.790328561392666, -27.59018479545873],
          [24.80268818053329, -27.58288180594306],
          [24.81092792662704, -27.567056993780913],
          [24.75599628600204, -27.508607155782826],
          [24.738143502798916, -27.514697130897716],
          [24.72578388365829, -27.532965033096218],
          [24.705184518423916, -27.562187361647396],
          [24.69282489928329, -27.59627024850316],
          [24.70106464537704, -27.615741427797115],
          [24.73402362975204, -27.61209084526035],
          [24.743636666861416, -27.62547571967499],
          [24.70106464537704, -27.64007553470646],
          [24.67909198912704, -27.659538924478802],
          [24.66810566100204, -27.6887275123932],
          [24.680465280142666, -27.71304537681072],
          [24.70106464537704, -27.721555348922188],
          [24.705184518423916, -27.745865894894138],
          [24.696944772330166, -27.78839629503583],
          [24.69557148131454, -27.802974318988497],
          [24.71754413756454, -27.813906553629074],
          [24.779342233267666, -27.886759984989332],
          [24.79275012793895, -27.90218116928733],
          [24.810602911142077, -27.922204424412513],
          [24.81678272071239, -27.935551201379933],
          [24.79206348243114, -27.945256912915184],
          [24.735758550790514, -27.964665719488632],
          [24.702799566415514, -27.982858306056414],
          [24.669840582040514, -27.999835284900435],
          [24.650614507821764, -28.014384852612626],
          [24.647867925790514, -28.031356864152194],
          [24.642374761728014, -28.039841866403265],
          [24.61628223243114, -28.045902172596353],
          [24.5977428037202, -28.050750171693185],
          [24.579203375009264, -28.04165999411288],
          [24.56684375586864, -28.04105395495732],
          [24.568217046884264, -28.057415813567268],
          [24.57851672950145, -28.067716447153607],
          [24.629328497079577, -28.098006704812327]]]);
```

```{code-block} javascript
// Get  collection
var sentinel2_level1c = ee.ImageCollection("COPERNICUS/S2");

// Get monthly clear Sentinel-2 Level-1C images for November 2016 - April 2017  
var nov_2016 = ee.Image('COPERNICUS/S2/20161126T080252_20161126T082438_T35JKK')
 .clip(vaalharts_irrigation_scheme);

var dec_2016 = ee.Image('COPERNICUS/S2/20161229T081332_20161229T083640_T35JKK')
 .clip(vaalharts_irrigation_scheme);

var jan_2017 = ee.Image('COPERNICUS/S2/20170128T081201_20170128T083151_T35JKK')
 .clip(vaalharts_irrigation_scheme);

var feb_2017 = ee.Image('COPERNICUS/S2/20170217T081001_20170217T083329_T35JKK')
 .clip(vaalharts_irrigation_scheme);

var mar_2017 = ee.Image('COPERNICUS/S2/20170326T080001_20170326T082243_T35JKK')
 .clip(vaalharts_irrigation_scheme);

var apr_2017 = ee.Image('COPERNICUS/S2/20170428T081011_20170428T083712_T35JKK')
 .clip(vaalharts_irrigation_scheme);

// Display images in Console
// print(nov_2016);
// print(dec_2016);
// print(jan_2017);
// print(feb_2017);
// print(mar_2017);
// print(apr_2017);
```

## Data Processing

```{code-block} javascript
// Aggregate Canny Edges (R/G/B/NIR for all months)
var canny_agg_nov_2016 = aggregate_canny_edges(nov_2016, 500, 1.5);
var canny_agg_dec_2016 = aggregate_canny_edges(dec_2016, 500, 1.5);
var canny_agg_jan_2017 = aggregate_canny_edges(jan_2017, 500, 1.5);
var canny_agg_feb_2017 = aggregate_canny_edges(feb_2017, 500, 1.5);
var canny_agg_mar_2017 = aggregate_canny_edges(mar_2017, 500, 1.5);
var canny_agg_apr_2017 = aggregate_canny_edges(apr_2017, 500, 1.5);

// Display Canny aggregates in Console
// print(canny_agg_nov_2016);
// print(canny_agg_dec_2016);
// print(canny_agg_jan_2017);
// print(canny_agg_feb_2017);
// print(canny_agg_mar_2017);
// print(canny_agg_apr_2017);

// Aggregate all Canny aggregates into single image
var canny_agg_all = canny_agg_nov_2016
  .add(canny_agg_dec_2016)
  .add(canny_agg_jan_2017)
  .add(canny_agg_feb_2017)
  .add(canny_agg_mar_2017)
  .add(canny_agg_apr_2017);

// Display new aggregate in Console
// print(canny_agg_all);

// Mask non-edge pixels
var edges = canny_agg_all.updateMask(canny_agg_all.gt(0));
// print(edges);

// Convert edges raster to vector
var edges_vector = raster_to_vector(edges.int(), vaalharts_irrigation_scheme, 1e8);
// NOTE: Printing the edges_vector to Console or adding to the map causes a memory limit error
```

## Data Postprocessing

```{code-block} javascript
// No data postprocessing in this lab.
```

## Data Visualization

```{code-block} javascript
// Set map options
Map.setCenter( 24.769355, -27.768264, 11);
Map.setOptions('SATELLITE');

// Add indvidual Canny aggregates to map
Map.addLayer(canny_agg_nov_2016, {}, 'Canny 4-Band Aggregate - Nov 2016');
Map.addLayer(canny_agg_dec_2016, {}, 'Canny 4-Band Aggregate - Dec 2016');
Map.addLayer(canny_agg_jan_2017, {}, 'Canny 4-Band Aggregate - Jan 2017');
Map.addLayer(canny_agg_feb_2017, {}, 'Canny 4-Band Aggregate - Feb 2017');
Map.addLayer(canny_agg_mar_2017, {}, 'Canny 4-Band Aggregate - Mar 2017');
Map.addLayer(canny_agg_apr_2017, {}, 'Canny 4-Band Aggregate - Apr 2017');

// Add all-month aggregate to map
Map.addLayer(canny_agg_all, {}, 'Canny 4-Band Aggregate - All Months');

// Add aedges (without background to map)
Map.addLayer(edges, {palette: ['white']}, 'Canny Edges - No Background');
```

## Data Export

```{code-block} javascript
// Export edges - Raster
var raster_export = export_raster(edges,vaalharts_irrigation_scheme, 10, 1e8, 'edges_raster');

// Export edges - Vector
var vector_export = export_vector(edges_vector, 'edges_vector');
```

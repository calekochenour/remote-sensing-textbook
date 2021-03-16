# Chapter 25: Rice Fields in Columbia

## Functions

```{code-block} javascript
// HELPER FUNCTIONS
/**
 * Mask Landsat 8 image with cloud and shadow masks
 * @param  {ee.image} image - Landsat 8 image
 * @return {ee.Image}       - Masked Landsat 8 image
 *
 * Function adapted from:
 * https://developers.google.com/earth-engine/datasets/catalog LANDSAT_LC08_C01_T1_SR
 */
function maskL8sr(image) {
  // Bits 3 and 5 are cloud shadow and cloud, respectively
  var cloudShadowBitMask = (1 << 3);
  var cloudsBitMask = (1 << 5);

  // Get the pixel QA band.
  var qa = image.select('pixel_qa');

  // Both flags should be set to zero, indicating clear conditions
  var mask = qa
    .bitwiseAnd(cloudShadowBitMask).eq(0)
    .and(qa.bitwiseAnd(cloudsBitMask).eq(0));

  // Mask image with clouds and shadows
  return image.updateMask(mask);
}

/**
 * Calculate and add NDVI band to Landsat 8 image
 * @param  {ee.image} image - Landsat 8 image
 * @return {ee.Image}       - Landsat 8 image with NDVI band added, named 'NDVI'
 */
function addNDVI(image) {
  // Calculate NDVI band
  var ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI');

  // Add NDVI band to image
  return image.addBands(ndvi);
}

/**
 * Convert ImageCollection into list
 * @param  {ee.ImageCollection} collection - Collection of images
 * @return {ee.List}                       - List of images
 */
function imageCollectionToList(collection) {
  // Turn an ImageCollection into a list
  return collection.toList(collection.size());
}

/**
 * Compute NDVI difference between two images
 * @param  {ee.List} collectionAsList - List of images
 * @param  {number}  postImageIndex   - Index of the post-change image
 * @param  {number}  preImageIndex    - Index of the pre-change image
 * @return {image}                    - NDVI difference (dNDVI) image
 */
function ndviDiff(collectionAsList, postImageIndex, preImageIndex) {
  // Get post-change NDVI band
  var postImageNDVI = ee.Image(
    collectionAsList.get(postImageIndex)).select('NDVI');

  // Get pre-change NDVI band  
  var preImageNDVI = ee.Image(
    collectionAsList.get(preImageIndex)).select('NDVI');

  // Compute difference (post-pre)
  return postImageNDVI.subtract(preImageNDVI);
}

// MAIN FUNCTIONS
/**
 * Create NDVI difference between two Landsat 8 images in an ImageCollection
 * Depends on helper functions
 * @param  {ee.ImageCollection} imageCollection - Collection of Landsat 8 images
 * @param  {number}             indexPost       - Index of the post-change image
 * @param  {number}             indexPre        - Index of the pre-change image
 * @return {image}                              - NDVI difference (dNDVI) image
 */
function computeNDVIDiffL8(imageCollection, indexPost, indexPre) {

  // Mask clouds and shadows for each image in the collection
  var collectionMasked = imageCollection.map(maskL8sr);

  // Add NDVI band to each image in the collection
  var collectionNDVI = collectionMasked.map(addNDVI);

  // Convert ImageCollection into list
  var collectionList = imageCollectionToList(collectionNDVI);

  // Compute NDVI difference for specified image indices in the collection
  var difference = ndviDiff(collectionList, indexPost, indexPre);

  // Return NDVI difference
  return difference;
}

/**
 * Segment and classify one-band NDVI difference image with object-based
 * image analysis (OBIA) with Simple Non-Iterative Clustering (SNIC) based
 * on NDVI thresholds
 * @param  {ee.Image}             imageDiffNDVI     - NDVI difference (dNDVI) image
 * @param  {ee.FeatureCollection} studyAreaBoundary - Study area to clip imagery
 * @param  {array}                thresholdValues   - 4-value array with NDVI thresholds
 *                                                    [primary min, primary max, secondary min, secondary max]
 * @return {object}               riceFields        - Primary and secondary rice field candidates                      
 */
function segmentOBIA(imageDiffNDVI, studyAreaBoundary, thresholdValues) {

  // Create seed points within study area boundary
  var seeds = ee.Algorithms.Image.Segmentation.seedGrid(24).clip(studyAreaBoundary);

  // Segment based on SNIC (Simple Non-Iterative Clustering)
  var snic = ee.Algorithms.Image.Segmentation.SNIC({
    image: imageDiffNDVI,
    size: 36,
    compactness: 5,
    connectivity: 8,
    neighborhoodSize: 256,
    seeds: seeds
  }).select(
    ['NDVI_mean', 'clusters'],
    ['NDVI', 'clusters']);

  // Select the clusters
  var clusters = snic.select('clusters');

  // Add clusters to the NDVI image
  imageDiffNDVI = imageDiffNDVI.addBands(clusters);

  // Compute per-cluster means
  var clustersMeanReduce = imageDiffNDVI.reduceConnectedComponents(
    ee.Reducer.mean(), 'clusters', 256);

  // Define primary and secondary candidates based on thresholds
  var riceFieldsPrimary = clustersMeanReduce
    .select("NDVI").gte(thresholdValues[0])
    .and(clustersMeanReduce.select("NDVI").lte(thresholdValues[1]));

  var riceFieldsSecondary = clustersMeanReduce
    .select("NDVI").gte(thresholdValues[2])
    .and(clustersMeanReduce.select("NDVI").lte(thresholdValues[3]));

  // Mask non-rice field clusters
  riceFieldsPrimary = riceFieldsPrimary.updateMask(riceFieldsPrimary);
  riceFieldsSecondary = riceFieldsSecondary.updateMask(riceFieldsSecondary);  

  // Store rice fields in object
  var riceFields = {
    "primary" : riceFieldsPrimary,
    "secondary": riceFieldsSecondary
  };

  // Return object
  return riceFields;
}

/**
 * Convert raster to vector
 * @param  {ee.Image}             objectsRaster - Primary or secondary rice field candidates
 * @param  {ee.FeatureCollection} studyArea     - Study area boundary
 * @return {ee.FeatureCollection} objectsVector - Rice fields coverted to vector feature
 */
function rasterToVector(objectsRaster, studyArea){

  // Convert objects (raster) to vectors
  var objectsVector = objectsRaster.reduceToVectors({
    geometry: studyArea,
    maxPixels: 20000000,
    scale: 5
  });

  // Return vectors
  return objectsVector;
}

/**
 * Merge and unionize feature collections
 * @param  {ee.FeatureCollection} riceFieldsPrimary   - Primary rice field candidates
 * @param  {ee.FeatureCollection} riceFieldsSecindary - Primary rice field candidates
 * @return {ee.FeatureCollection} combinedFields      - Combined/merged rice fields
 */
function combineRiceFields(riceFieldsPrimary, riceFieldsSecondary){

  // Merge rice field candidates and create union
  var merge = riceFieldsPrimary.merge(riceFieldsSecondary);
  var combinedFields = merge.union(ee.ErrorMargin(1));

  // Return combined rice field candidates
  return combinedFields;
}

/**
 * Export vector as shapefile to Google Drive or to GEE Asset
 * @param  {ee.FeatureCollection} vector        - Vector that will be exported
 * @param  {string}               outputName    - Name of the output file (without extension)
 * @param  {string}               outputMethod  - Name of the export method/location ("Drive" for Google Drive, "Asset" for GEE Asset)
 * @return {string}               outputMessage - Message indicating the task to run to complete the export
 */
function exportVector(vector, outputName, outputMethod){

  // Create variable for output message
  var outputMessage;

  if (outputMethod.toLowerCase() == "drive") {

    // Export vectors as shapefile to Google Drive
    Export.table.toDrive({
      collection: vector,
      description: outputName,
      fileFormat: 'SHP'
    });

    // Assign output message
    outputMessage = "Task ready: " + outputName + "\nPlease run task to export to Google Drive.";

  } else if (outputMethod.toLowerCase() == "asset") {

    // Export vectors to GEE Asset
    Export.table.toAsset({
      collection: vector,
      description: outputName,
      assetId: outputName
    });

     // Assign output message
    outputMessage = "Task ready: " + outputName + "\nPlease run task to export to GEE Asset.";

  } else {

     // Assign output message
    outputMessage = "Invalid export method. Please specify 'Drive' or 'Asset'.";

  }

  // Return output message
  return outputMessage;
}
```

## Data Acquisition & Preprocessing

```{code-block} javascript
// Define study area boundary and study area canals
var drtt = ee.FeatureCollection("users/calekochenour/vegetation-change/drtt_study_area_boundary");
var canals = ee.FeatureCollection("users/calekochenour/vegetation-change/drtt_study_area_canals");

// Load and clip imagery
var peakGreen = ee.Image('LANDSAT/LC08/C01/T1_SR/LC08_008057_20181230').clip(drtt);
var harvest = ee.Image('LANDSAT/LC08/C01/T1_SR/LC08_008057_20190216').clip(drtt);
var postHarvest = ee.Image('LANDSAT/LC08/C01/T1_SR/LC08_008057_20190304').clip(drtt);

// Create ImageCollection from individual images
var collection = ee.ImageCollection([peakGreen, harvest, postHarvest]);
```

## Data Processing

```{code-block} javascript
// COMPUTE NDVI DIFFERENCE
// Compute Peak Green to Harvest NDVI difference
var ndviDiffGreenHarvest = computeNDVIDiffL8(collection, 1, 0);

// Compute Peak Green to Post-Harvest NDVI difference
var ndviDiffGreenPostHarvest = computeNDVIDiffL8(collection, 2, 0);

// SEGMENT AND CLASSIFY NDVI DIFFERENCE
// Define NDVI thresholds (primMin, primMax, secMin, secMax)
var ndviThresholds = [-2.0, -0.35, -0.35, -0.1];

// Segment/classify
var ndviSegments = segmentOBIA(
  ndviDiffGreenPostHarvest,
  drtt,
  ndviThresholds
);

// CONVERT CLASSIFIED RASTER OBJECTS TO VECTORS
// Convert objects (raster) to vectors
var vectorPrimary = rasterToVector(
  ndviSegments.primary,
  drtt   
);

var vectorSecondary = rasterToVector(
  ndviSegments.secondary,
  drtt   
);

// Combine primary and secondary candidates
var vectorRiceFields = combineRiceFields(
  vectorPrimary,
  vectorSecondary
);
```

## Data Postprocessing

```{code-block} javascript
// No data postprocessing in this lab.
```

## Data Visualization

```{code-block} javascript
// Zoom to study area
Map.setCenter(-75.0978, 3.7722, 12);

// Create empty image into which to paint the features; create outlines of drtt and canals
var empty = ee.Image().byte();

var studyAreaOutline = empty.paint({
  featureCollection: drtt,
  color: 1,
  width: 3
});

var canalOutline = empty.paint({
  featureCollection: canals,
  color: 1,
  width: 3
});


// Define visualization parameters for RGB
var landsat8RGBVisParams = {
  bands: ['B4', 'B3', 'B2'],
  min: 0,
  max: 2500
};

// Define visualization parameters for NDVI
var ndviVisParams = {
  min: -1,
  max: 1,
  palette: ['blue', 'white', 'green']
};

// Define visualization parameters for NDVI difference
var ndviDiffVisParams = {
  min: -2,
  max: 2,
  palette: ['red', '#ece6d6', 'green']
};

/**
* Create Styled Layer Descriptor (SLD) for NDVI ranges. This allows
* for discrete intervals that are mapped to colors, which can highlight
* certain categories of NDVI change. The values and number of categories
* are context-depedent.
*/
var ndviSLD =
  '<RasterSymbolizer>' +
    '<ColorMap  type="interval" extended="false" >' +
      '<ColorMapEntry color="#d7191c" quantity="-2" label=""/>' +
      '<ColorMapEntry color="#fdae61" quantity="-0.5" label=""/>' +
      '<ColorMapEntry color="#ece6d6" quantity="-0.25" label=""/>' +
      '<ColorMapEntry color="#ece6d6" quantity="0.25" label="" />' +
      '<ColorMapEntry color="#a6d96a" quantity="0.5" label=""/>' +
      '<ColorMapEntry color="#1a9641" quantity="2" label="" />' +
    '</ColorMap>' +
  '</RasterSymbolizer>';

// Add study area boundary and canals to map
Map.addLayer(
  studyAreaOutline,
  {palette: 'FF0000'},
  'Study Area');

Map.addLayer(
  canalOutline,
  {palette: '0000FF'},
  'Canals');

// Add imagery to map
Map.addLayer(
  peakGreen,
  landsat8RGBVisParams,
  "Peak Green",
  false
);

Map.addLayer(
  harvest,
  landsat8RGBVisParams,
  "Harvest",
  false
);

Map.addLayer(
  postHarvest,
  landsat8RGBVisParams,
  "Post Harvest",
  false
);

// Add NDVI difference to map - continious color ramp
Map.addLayer(
  ndviDiffGreenHarvest,
  ndviDiffVisParams,
  "NDVI Diff - Green to Harvest",
  false
);

Map.addLayer(
  ndviDiffGreenPostHarvest,
  ndviDiffVisParams,
  "NDVI Diff - Green to Post Harvest",
  false
);

// Add NDVI difference to map - discrete color ramp
Map.addLayer(
  ndviDiffGreenHarvest.sldStyle(ndviSLD),
  {},
  'NDVI intervals - 5 categories - Peak Green to Harvest',
  false);

Map.addLayer(
  ndviDiffGreenPostHarvest.sldStyle(ndviSLD),
  {},
  'NDVI intervals - 5 categories - Peak Green to Post Harvest');

// Add primary and secondary rice field candidates to map
Map.addLayer(
ndviSegments.primary,
  {palette: ['green']},
  "OBIA - Rice Fields - Primary - Peak Green to Post-Harvest", false);

Map.addLayer(
  ndviSegments.secondary,
  {palette: ['lightgreen']},
  "OBIA - Rice Fields - Secondary - Peak Green to Post-Harvest", false);

// Add primary, secondary, and combined rice fields to map
Map.addLayer(
  vectorPrimary,
  {color: 'green'},
  "Vector - Rice Fields - Primary",
  false);

Map.addLayer(
  vectorSecondary,
  {color: 'lightgreen'},
  "Vector - Rice Fields - Secondary",
  false);

Map.addLayer(
  vectorRiceFields,
  {color: 'green'},
  "Vector - Rice Fields - Combined");
```

## Data Export

```{code-block} javascript
// Create export tasks for primary, secondary, and combined rice fields
var exportPrimary = exportVector(
  vectorPrimary,
  "rice_fields_2018_semester_b_primary",
  "Drive"
);

var exportSecondary = exportVector(
  vectorSecondary,
  "rice_fields_2018_semester_b_secondary",
  "Drive"
);

var exportCombined = exportVector(
  vectorRiceFields,
  "rice_fields_2018_semester_b_combined",
  "Drive"
);

// Display task creation output to console - still need to run tasks
print(exportPrimary);
print(exportSecondary);
print(exportCombined);

// Export NDVI difference image
Export.image.toDrive({
  image: ndviDiffGreenPostHarvest,
  description: 'ndvi_difference_20181230_20190304',
  scale: 30,
  region: drtt
});
```

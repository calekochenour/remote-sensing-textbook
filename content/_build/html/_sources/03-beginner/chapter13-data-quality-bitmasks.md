# Chapter 13: Data Quality Bitmasks

This chapter provides a workflow to explore quality flag bitmasks for imagery in Rocky Mountain National Park, Colorado, United States. The full GEE code can be found [here](https://code.earthengine.google.com/3abc12c776843589171290807d35c5c2).

Code for functions was adapted from this [Geographic Information Systems Stack Exchange](https://gis.stackexchange.com/questions/292835/using-cloud-confidence-to-create-cloud-mask-from-landsat-8-bqa) post and this [Open Geo Blog](https://mygeoblog.com/2019/07/25/working-with-bitmasks/) post.

## Functions

```{code-block} javascript
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
```

## Data Acquisition & Preprocessing

Landsat 8 T1 SR 'pixel_qa' band bitmasks:

* Bit 0: Fill
* Bit 1: Clear
* Bit 2: Water
* Bit 3: Cloud Shadow
* Bit 4: Snow
* Bit 5: Cloud
* Bits 6-7: Cloud Confidence
    * 0: None
    * 1: Low
    * 2: Medium
    * 3: High
* Bits 8-9: Cirrus Confidence
    * 0: None
    * 1: Low
    * 2: Medium
    * 3: High
* Bit 10: Terrain Occlusion

Bitmask value of 1 for single bits means flag is set (i.e. water == 1 --> pixel is water). Bitmask value for multiple bits indicates condition (cirrus confidence of 3).

```{code-block} javascript
// Define RMNP Boundary
var rmnp_boundary = ee.FeatureCollection("users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon");

// Define Landsat 8 collection
var landsat8_t1_sr = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR');

// Get single image for QA evaluation
var rmnp = landsat8_t1_sr
  .filter(ee.Filter.calendarRange(2013, 2020, 'year'))
  .filter(ee.Filter.calendarRange(6, 9, 'month'))
  .filterBounds(rmnp_boundary)
  .first()
  .clip(rmnp_boundary);

print('Baseline Image', rmnp);

// Get the pixel QA band
var rmnp_qa = rmnp.select('pixel_qa');
print('QA Band:', rmnp_qa);

// EXTRACT QA BITS
// Fill bitmask (bit 0)
var fill_quality = extract_qa_bits(rmnp_qa, 0, 0, 'fill_bitmask');
print('Fill Bitmask (Bit 0):', fill_quality);

// Clear bitmask (bit 1)
var clear_quality = extract_qa_bits(rmnp_qa, 1, 1, 'clear_bitmask');
print('Clear Bitmask (Bit 1):', clear_quality);

// Water bitmask (bit 2)
var water_quality = extract_qa_bits(rmnp_qa, 2, 2, 'water_bitmask');
print('Water Bitmask (Bit 2):', water_quality);

// Cloud shadow bitmask (bit 3)
var cloud_shadow_quality = extract_qa_bits(rmnp_qa, 3, 3, 'cloud_shadow_bitmask');
print('Cloud Shadow Bitmask: (Bit 3)', cloud_shadow_quality);

// Snow bitmask (bit 4)
var snow_quality = extract_qa_bits(rmnp_qa, 4, 4, 'snow_bitmask');
print('Snow Bitmask (Bit 4):', snow_quality);

// Cloud bitmask (bit 5)
var cloud_quality = extract_qa_bits(rmnp_qa, 5, 5, 'cloud_bitmask');
print('Cloud Bitmask (Bit 5):', cloud_quality);

// Cloud confidence bitmask (bits 6-7)
var cloud_confidence_quality = extract_qa_bits(rmnp_qa, 6, 7, 'cloud_confidence_bitmask');
print('Cloud Confidence Bitmask (Bits 6-7):', cloud_confidence_quality);

// Cirrus confidence bitmask (bits 8-9)
var cirrus_confidence_quality = extract_qa_bits(rmnp_qa, 8, 9, 'cirrus_confidence_bitmask');
print('Cirrus Confidence Bitmask (Bits 8-9):', cirrus_confidence_quality);

// Terrain occlusion bitmask (bit 10)
var terrain_occlusion_quality = extract_qa_bits(rmnp_qa, 10, 10, 'terrain_occlusion_bitmask');
print('Terrain Occlusion Bitmask (Bit 10):', terrain_occlusion_quality);

// MASK PIXELS BASED ON VARIOUS BITMASK FLAGS (CLOUD & SHADOW, CLEAR, ETC.)
// Clear pixels
var rmnp_masked_clear = rmnp.updateMask(clear_quality.eq(1)); // 1 means clear pixel

// Shadows and clouds (indicates shadow free AND cloud free)
var rmnp_masked_shadows_clouds = rmnp.updateMask(
  cloud_shadow_quality.eq(0).and(cloud_quality.eq(0)));

// Shadows only
var rmnp_masked_shadows = rmnp.updateMask(cloud_shadow_quality.eq(0));

// Snow
var rmnp_masked_snow = rmnp.updateMask(snow_quality.eq(0));

// Clouds only
var rmnp_masked_clouds = rmnp.updateMask(cloud_quality.eq(0));
```

## Data Processing

```{code-block} javascript
// No data processing in this lab.
```

## Data Postprocessing
```{code-block} javascript
// No data post-processing in this lab.
```

## Data Visualization

```{code-block} javascript
// Define Landsat 8 RGB visualization parameters
var l8_vis_params_rgb = {
  'bands': ['B4', 'B3', 'B2'],
  'min': 0,
  'max': 3000
};

// Define Landsat 8 CIR visualization parameters
var l8_vis_params_cir = {
  'bands': ['B5', 'B4', 'B3'],
  'min': 0,
  'max': 3000
};

// Center map to Rocky Mountain National Park, Colorado
Map.setCenter(-105.6836, 40.3428, 10);

// Baseline image
Map.addLayer(rmnp, l8_vis_params_rgb, 'RMNP Baseline Image');

// Pixel QA band
Map.addLayer(rmnp_qa, {}, 'QA Band', false);

// Bitmask layers
Map.addLayer(fill_quality, {min: 0, max: 1}, 'Fill Bitmask');
Map.addLayer(clear_quality, {min: 0, max: 1}, 'Clear Bitmask');
Map.addLayer(water_quality, {min: 0, max: 1}, 'Water Bitmask');
Map.addLayer(cloud_shadow_quality, {min: 0, max: 1}, 'Cloud Shadow Bitmask');
Map.addLayer(snow_quality, {min: 0, max: 1}, 'Snow Bitmask');
Map.addLayer(cloud_quality, {min: 0, max: 1}, 'Cloud Bitmask');
Map.addLayer(cloud_confidence_quality, {min: 0, max: 3}, 'Cloud Confidence Bitmask');
Map.addLayer(cirrus_confidence_quality, {min: 0, max: 3}, 'Cirrus Confidence Bitmask');
Map.addLayer(terrain_occlusion_quality, {min: 0, max: 1}, 'Terrain Occlusion Bitmask');

// Masked layers
Map.addLayer(rmnp_masked_clear, l8_vis_params_rgb, 'Masked for Clear Pixels');
Map.addLayer(rmnp_masked_shadows_clouds, l8_vis_params_rgb, 'Masked for Shadow and Cloud Pixels');
Map.addLayer(rmnp_masked_shadows, l8_vis_params_rgb, 'Masked for Shadow Pixels');
Map.addLayer(rmnp_masked_snow, l8_vis_params_rgb, 'Masked for Snow Pixels');
Map.addLayer(rmnp_masked_clouds, l8_vis_params_rgb, 'Masked for Cloud Pixels');
```

## Data Export
```{code-block} javascript
// No data export in this lab.
```

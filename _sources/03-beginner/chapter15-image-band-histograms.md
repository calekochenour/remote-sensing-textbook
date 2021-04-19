# Chapter 15: Image Band Histograms

This chapter provides a workflow to explore image band histograms for an area near Lake Champlain and Burlington, Vermont, United States. The full GEE code can be found [here](https://code.earthengine.google.com/1abf63773d0dffdf0713fccda71d73c2).

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
 * Calculate and add NDWI band to Landsat 8 image
 * @param  {ee.Image} image - Landsat 8 image
 * @return {ee.Image}       - Landsat 8 image with NDWI band added
 */
var add_ndwi = function(image) {
  var ndvi = image.normalizedDifference(['B3', 'B5']).rename('NDWI');
  return image.addBands(ndvi);
};
```

## Data Acquisition & Preprocessing

```{code-block} javascript
// Define AOI (near Lake Champlain and Burlington, Vermont)
var vermont_aoi =
    /* color: #d60000 */
    /* shown: false */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[-73.45522034657436, 44.63572796451827],
          [-73.45522034657436, 44.326105640920396],
          [-72.95808899891811, 44.326105640920396],
          [-72.95808899891811, 44.63572796451827]]], null, false);

// Check map scale at different zoom levels
// Get least cloudy image and clip to AOI
var vermont_l8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
  .filterDate('2020-06-01', '2020-08-30')
  .filterBounds(vermont_aoi)
  .sort('CLOUD_COVER')
  .first()
  .clip(vermont_aoi);

// Add NDVI and NDWI band
vermont_l8 = add_ndwi(add_ndvi(vermont_l8));
print('Landsat 8:', vermont_l8);

// Create histograms
// B1
var histogram_b1 = ui.Chart.image.histogram({
  image: vermont_l8.select('B1'),
  region: vermont_aoi,
  scale: 30,
  minBucketWidth: 50
});
histogram_b1.setOptions({
  title: 'B1'
});

// B2
var histogram_b2 = ui.Chart.image.histogram({
  image: vermont_l8.select('B2'),
  region: vermont_aoi,
  scale: 30,
  minBucketWidth: 50
});
histogram_b2.setOptions({
  title: 'B2'
});

// B3
var histogram_b3 = ui.Chart.image.histogram({
  image: vermont_l8.select('B3'),
  region: vermont_aoi,
  scale: 30,
  minBucketWidth: 50
});
histogram_b3.setOptions({
  title: 'B3'
});

// B4
var histogram_b4 = ui.Chart.image.histogram({
  image: vermont_l8.select('B4'),
  region: vermont_aoi,
  scale: 30,
  minBucketWidth: 50
});
histogram_b4.setOptions({
  title: 'B4'
});

// B5
var histogram_b5 = ui.Chart.image.histogram({
  image: vermont_l8.select('B5'),
  region: vermont_aoi,
  scale: 30,
  minBucketWidth: 50
});
histogram_b5.setOptions({
  title: 'B5'
});

// B6
var histogram_b6 = ui.Chart.image.histogram({
  image: vermont_l8.select('B6'),
  region: vermont_aoi,
  scale: 30,
  minBucketWidth: 50
});
histogram_b6.setOptions({
  title: 'B6'
});

// B7
var histogram_b7 = ui.Chart.image.histogram({
  image: vermont_l8.select('B7'),
  region: vermont_aoi,
  scale: 30,
  minBucketWidth: 50
});
histogram_b7.setOptions({
  title: 'B7'
});

// B10
var histogram_b10 = ui.Chart.image.histogram({
  image: vermont_l8.select('B10'),
  region: vermont_aoi,
  scale: 30,
});
histogram_b10.setOptions({
  title: 'Histogram of B10'
});

// B11
var histogram_b11 = ui.Chart.image.histogram({
  image: vermont_l8.select('B11'),
  region: vermont_aoi,
  scale: 30,
});
histogram_b11.setOptions({
  title: 'B11'
});

// SR Aerosol
var histogram_sr_aerosol = ui.Chart.image.histogram({
  image: vermont_l8.select('sr_aerosol'),
  region: vermont_aoi,
  scale: 30,
});
histogram_sr_aerosol.setOptions({
  title: 'SR Aerosol'
});

// Pixel QA
var histogram_pixel_qa = ui.Chart.image.histogram({
  image: vermont_l8.select('pixel_qa'),
  region: vermont_aoi,
  scale: 30,
});
histogram_pixel_qa.setOptions({
  title: 'Pixel QA'
});

// Radsat QA
var histogram_radsat_qa = ui.Chart.image.histogram({
  image: vermont_l8.select('radsat_qa'),
  region: vermont_aoi,
  scale: 30,
});
histogram_radsat_qa.setOptions({
  title: 'Radsat QA'
});

// NDVI
var histogram_ndvi = ui.Chart.image.histogram({
  image: vermont_l8.select('NDVI'),
  region: vermont_aoi,
  scale: 30,
});
histogram_ndvi.setOptions({
  title: 'NDVI'
});

// NDWI
var histogram_ndwi = ui.Chart.image.histogram({
  image: vermont_l8.select('NDWI'),
  region: vermont_aoi,
  scale: 30,
});
histogram_ndwi.setOptions({
  title: 'NDWI'
});
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
// Center and zoom map
Map.setCenter(-73.222849, 44.477142, 10);

// Add RGB image to map
Map.addLayer(
  vermont_l8,
  {'bands': ['B4', 'B3', 'B2'], min: 0, max: 1500},
  'Landsat 8 - RGB - July 6, 2020'
);

// Add NDVI to map
Map.addLayer(
  vermont_l8,
  {'bands': ['NDVI'], palette: ['blue', 'white', 'green'], min: -1, max: 1},
  'Landsat 8 - NDVI - July 6, 2020',
  false
);

// Add NDWI to map
Map.addLayer(
  vermont_l8,
  {'bands': ['NDWI'], palette: ['00FFFF', '0000FF'], min: -1, max: 1},
  'Landsat 8 - NDWI - July 6, 2020',
  false
);

// Add histograms to Console
print(histogram_b1);
print(histogram_b2);
print(histogram_b3);
print(histogram_b4);
print(histogram_b5);
print(histogram_b6);
print(histogram_b7);
print(histogram_b10);
print(histogram_b11);
print(histogram_sr_aerosol);
print(histogram_pixel_qa);
print(histogram_radsat_qa);
print(histogram_ndvi);
print(histogram_ndwi);
```

## Data Export

```{code-block} javascript
// No data export in this lab.
```

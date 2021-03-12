# Chapter 14: Image to Asset

## Data Acquisition & Preprocessing

```{code-block} javascript
// Define boundary for Rocky Mountain National Park, Colorado
var rmnp_boundary = ee.FeatureCollection("users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon");

// Filter Landsat 8 to single image
var rmnp_image = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
  .filterDate('2018-07-01', '2018-08-31')
  .filterBounds(rmnp_boundary)
  .sort('CLOUD_COVER')
  .first()
  .clip(rmnp_boundary);
print("Original Image:", rmnp_image);
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
// No data visualization in this lab.
```

## Data Export

```{code-block} javascript
// Export image to asset
Export.image.toAsset({
  image: rmnp_image,
  description: "test-image-task", // Task name
  assetId: 'images/test-image', // "images" is an image collection within assets
  scale: 30,
  maxPixels: 1e13
});

// Load and print image asset
var rmnp_image_from_asset = ee.Image("users/{username}/images/test-image");
print("Image from Assets:", rmnp_image_from_asset);
```

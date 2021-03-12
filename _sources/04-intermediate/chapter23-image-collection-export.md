# Chapter 23: Image Collection Export

Resources:

* [geetools-code-editor GitHub](https://github.com/fitoprincipe/geetools-code-editor)
* [geetools-code-editor Batch module](https://github.com/fitoprincipe/geetools-code-editor/blob/master/batch)
* [geetools-code-editor Batch module wiki](https://github.com/fitoprincipe/geetools-code-editor/wiki/Batch)

## Functions

```{code-block} javascript
// Import geetools-code-editor Batch module
var batch = require('users/fitoprincipe/geetools:batch');
```

## Data Acquisition & Preprocessing

```{code-block} javascript
// Set area of interest (AOI)
var rmnp_boundary = ee.FeatureCollection("users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon");
var colorado_boundary = ee.FeatureCollection("users/calekochenour/colorado_boundary");

// Filter Landsat 8 based on dates and AOI
var rmnp_collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
  .filterDate('2020-06-01', '2021-01-21')
  .filterBounds(rmnp_boundary);
print("Image Collection", rmnp_collection);
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
// Set export folder (relative to Google Drive root folder)
var output_folder = 'gee-export';

// Export collection image to Drive
batch.Download.ImageCollection.toDrive(
  rmnp_collection, // colorado_collection
  output_folder,
  {
    name: '{id}', // {id}, {system_date} and all other properties (e.g., {WRS_PATH})
    // dateFormat: 'yyyy-MM-dd', // Default
    scale: 30,
    maxPixels: 1e13,
    region: colorado_boundary, // rmnp_boundary,
    type: 'int16' // 'float', 'byte', 'int', 'double', 'long', 'short', 'int8',
                  // 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32'
  }
);

print("Completed script. Tasks are available to run.");
```

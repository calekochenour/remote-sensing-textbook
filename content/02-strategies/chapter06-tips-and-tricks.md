# Chapter 6: Tips and Tricks

This chapter provides useful (and possibly lesser known) tips and tricks.

GEE tasks still process when the computer is shut down (processing continues in the cloud). This means the user does not have to supervise the task processing while ongoing.

GEE methods to get metadata properties provide a useful way to learn about an image. These methods may also provide ideas for which properties to use for image collection reduction and filtering.

```{code-block} javascript
// Get all bands
var band_names = image.bandNames();
print('Band names: ', band_names);

// Get single band (Sentinel-2 MSI)
var red = image.select('B4');
print('Red band: ', band_names);

// Get multiple (but not all) bands (Sentinel-2 MSI)
var red_nir = image.select(['B4', 'B8']);
print("Red and NIR bands: ", red_nir);

// Get all metadata properties
var properties = image.propertyNames();
print('Metadata properties: ', properties);

// Get specific metadata property (Sentinel-2 MSI)
var cloudiness = image.get('CLOUDY_PIXEL_PERCENTAGE');
print('CLOUDY_PIXEL_PERCENTAGE: ', cloudiness);

// Get timestamp and convert to date
var date = ee.Date(image.get('system:time_start'));
print('Timestamp: ', date);

// Get object type
var image_type = image.name();
print('Image object type: ', image_type);

// Get image geometry
var image_geometry = image.geometry();
print('Image geometry:', image_geometry)
```

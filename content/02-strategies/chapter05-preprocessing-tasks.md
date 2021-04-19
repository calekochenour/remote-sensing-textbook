# Chapter 5: Preprocessing Tasks

This chapter provides an introduction to imagery preprocessing tasks.

## Find Imagery

Criteria to filter collections on include, but are not limited to:

* Location (point, bounding box, polygon AOI);
* Date or date range;
* Other metadata/image properties (cloud cover, sensing time, WRS path/row for Landsat); and/or,
* Sorting / getting first image (usually least cloudy).

## Create/Add Bands

This could be index layers and/or masks. Possible layers include, but are not limited to:

* NDVI;
* NDWI;
* NBR;
* Water mask (from manual thresholding / equation or quality band);
* Cloud mask (from manual thresholding / equation or quality band); and/or,
* Shadow mask (from manual thresholding / equation or quality band).

## Mask Pixels

Pixels for masking consideration include, but are not limited to:

* Water;
* Clouds;
* Shadows;
* Snow;
* Terrain Occlusion;
* Fill Value;
* Invalid Values (outside valid range);
* Sensor problems (radiometric saturation QA band and/or Saturate Value);
* Scene classification / land cover (from platform band and/or other dataset layers);
* Other QA bitmasks / flags (platform- or sensor-dependent, e.g., Mandatory Quality Flag); and/or,
* Custom (sensor band or index layers or sensor bands, e.g., NDVI < 0).

## Scale Data

Look for scale factor in the product specifications. Often a number of type float similar to 0.0001, 0.001, or 0.01, used to scale data to collected sensor values. Unscaled data (of type integer) reduces the data storage size, compared to scaled data (of type float).

## Clip Imagery

Clip the image or collection to the specific Area of Interest (AOI). This will reduce processing time of analysis tasks.

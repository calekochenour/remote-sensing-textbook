# Chapter 1: Landsat Collections

[Landsat](https://developers.google.com/earth-engine/datasets/catalog/landsat) platform.

Landsat processing [tiers](https://developers.google.com/earth-engine/guides/landsat#landsat-collection-structure).

## Landsat 8

[Landsat 8](https://developers.google.com/earth-engine/datasets/catalog/landsat-8) collection.

### Surface Reflectance (SR)

* USGS Landsat 8 Surface Reflectance Tier 1
* USGS Landsat 8 Surface Reflectance Tier 2

### Top of Atmosphere (TOA)

* USGS Landsat 8 Collection 1 Tier 1 TOA Reflectance
* USGS Landsat 8 Collection 1 Tier 1 and Real-Time data TOA Reflectance
* USGS Landsat 8 Collection 1 Tier 2 TOA Reflectance

### Raw Images

* USGS Landsat 8 Collection 1 Tier 1 Raw Scenes
* USGS Landsat 8 Collection 1 Tier 1 and Real-Time data Raw Scenes
* USGS Landsat 8 Collection 1 Tier 2 Raw Scenes

### Derived Datasets

* Burned Area Index (BAI)
* Enhanced Vegetation Index (EVI)
* Normalized Difference Vegetation Index (NDVI)
* Normalized Burn Ratio Thermal (NBRT)
* Normalized Difference Snow Index (NDSI)
* Normalized Difference Water Index (NDWI)

### Specifications and Quality

Section 6 of the Landsat 8 Collection 1 (C1) Land Surface Reflectance Code (LaSRC) [product guide](https://prd-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/atoms/files/LSDS-1368_L8_C1-LandSurfaceReflectanceCode-LASRC_ProductGuide-v3.pdf) provides information related to the SR specifications as well to the data quality measurements.

#### Surface Reflectance Specifications

```{table} Surface Reflectance Specifications
:name: table:landsat8-sr-specs

| Band Designation     | Band Name                      | Data Type               | Units       | Range         | Valid Range | Fill Value | Saturate Value | Scale Factor |
| :------------------- | :----------------------------- | :---------------------- | :---------- | :-------------  | :----------- |  :---------- | :--------------- | :------------- |
| ProductID_sr_band1   | Band 1                         | 16-Bit Signed Integer   | Reflectance | -2000 - 16000 | 0 - 10000   | -9999      | 20000          | 0.0001       |
| ProductID_sr_band2   | Band 2                         | 16-Bit Signed Integer   | Reflectance | -2000 - 16000 | 0 - 10000   | -9999      | 20000          | 0.0001       |
| ProductID_sr_band3   | Band 3                         | 16-Bit Signed Integer   | Reflectance | -2000 - 16000 | 0 - 10000   | -9999      | 20000          | 0.0001       |
| ProductID_sr_band4   | Band 4                         | 16-Bit Signed Integer   | Reflectance | -2000 - 16000 | 0 - 10000   | -9999      | 20000          | 0.0001       |
| ProductID_sr_band5   | Band 5                         | 16-Bit Signed Integer   | Reflectance | -2000 - 16000 | 0 - 10000   | -9999      | 20000          | 0.0001       |
| ProductID_sr_band6   | Band 6                         | 16-Bit Signed Integer   | Reflectance | -2000 - 16000 | 0 - 10000   | -9999      | 20000          | 0.0001       |
| ProductID_sr_band7   | Band 7                         | 16-Bit Signed Integer   | Reflectance | -2000 - 16000 | 0 - 10000   | -9999      | 20000          | 0.0001       |
| ProductID_pixel_qa   | Level 2 Quality Band           | 16-Bit Unsigned Integer | Bit Index   | 0 - 32768     | 0 - 32768   | 1 (Bit 0)  | NA             | NA           |
| ProductID_sr_aerosol | Aerosol QA                     | 8-Bit Unsigned Integer  | Bit Index   | 0 - 255       | 0 - 255     | NA        | NA             | NA           |
| ProductID_radsat_qa  | Radiometric Saturation QA      | 16-Bit Unsigned Integer | Bit Index   | 0 - 32768     | 0 - 32768   | 1 (Bit 0)  | NA             | NA           |
| ProductID_MTL.txt    | Level 1 Metadata File          | NA                     | NA          | NA            | NA          | NA         | NA             | NA           |
| ProductID_ANG.txt    | Level 1 Angle Coefficient File | NA                     | NA          | NA            | NA          | NA         | NA             | NA           |

```

#### Pixel Quality Assessment (QA) Band

```{table} Landsat 8 Pixel Quality Assessment Bit Index
:name: table:landsat8-pixel-qa-index

| Bit | Bit Value | Cumulative Sum | Attribute |
|:-|:-|:-|:-|
| 0 | 1 | 1 | Fill |
| 1 | 2 | 3 | Clear |
| 2 | 4 | 7 | Water |
| 3 | 8 | 15 | Cloud Shadow |
| 4 | 16 | 31 | Snow |
| 5 | 32 | 63 | Cloud |
| 6-7 | 64 / 128 | 127 / 255 | Cloud Confidence<br>00 (0) = None<br>01 (1) = Low<br>10 (2) = Medium<br>11 (3) = High |
| 8-9 | 256 / 512 | 511 / 1023 | Cirrus Confidence<br>00 (0) = Not Set<br>01 (1) = Low from OLI Band 9 Reflectance<br>10 (2) = Medium from OLI Band 9 Reflectance (Not Used)<br>11 (3) = High from OLI Band 9 Reflectance |
| 10 | 1024 | 2047 | Terrain Occlusion |
| 11 | 2048 | 4095 | Unused |
| 12 | 4096 | 8191 | Unused |
| 13 | 8192 | 16383 | Unused |
| 14 | 16384 | 32767 | Unused |
| 15 | 32768 | 655535 | Unused |

```

```{table} Landsat 8 Pixel Quality Assessment Values
:name: table:landsat8-pixel-qa-values

| Attribute | Pixel Value |
|:-|:-|
| Fill | 1 |
| Clear | 322, 386, 834, 898, 1346 |
| Water | 324, 388, 836, 900, 1348 |
| Cloud Shadow | 328, 392, 840, 904, 1350 |
| Snow/Ice | 336, 368, 400, 432, 848, 880, 912, 944, 1352 |
| Cloud | 352, 368, 416, 432, 480, 864, 880, 928, 944, 992 |
| Low Confidence Cloud | 322, 324, 328, 336, 352, 368, 834, 836, 840, 848, 864, 880 |
| Medium Confidence Cloud | 386, 388, 392, 400, 416, 432, 898, 900, 904, 928, 944 |
| High Confidence Cloud | 480, 992 |
| Low Confidence Cirrus | 322, 324, 328, 336, 352, 368, 386, 388, 392, 400, 416, 432, 480 |
| High Confidence Cirrus | 834, 836, 840, 848, 864, 880,898,900, 904, 912, 928, 944, 992 |
| Terrain Occlusion | 1346, 1348, 1350, 135 |

```

#### Radiometric Saturation QA Band

```{table} Landsat 8 Radiometric Saturation Quality Assessment Bit Index
:name: table:landsat8-radsat-qa-index

| Bit | Bit Value | Cumulative Sum | Description |
|:-|:-|:-|:-|
| 0 | 1 | 1 | Data Fill Flag (0 valid data, 1 invalid data) |
| 1 | 2 | 3 | Band 1 Data Saturation Flag (0 valid data, 1 saturated data) |
| 2 | 4 | 7 | Band 2 Data Saturation Flag (0 valid data, 1 saturated data) |
| 3 | 8 | 15 | Band 3 Data Saturation Flag (0 valid data, 1 saturated data) |
| 4 | 16 | 31 | Band 4 Data Saturation Flag (0 valid data, 1 saturated data) |
| 5 | 32 | 63 | Band 5 Data Saturation Flag (0 valid data, 1 saturated data) |
| 6 | 64 | 127 | Band 6 Data Saturation Flag (0 valid data, 1 saturated data) |
| 7 | 128 | 255 | Band 7 Data Saturation Flag (0 valid data, 1 saturated data) |
| 8 | NA | NA | Not Used |
| 9 | 512 | 1023 | Band 9 Data Saturation Flag (0 valid data, 1 saturated data) |
| 10 | 1024 | 2047 | Band 10 Data Saturation Flag (0 valid data, 1 saturated data) |
| 11 | 2048 | 4095 | Band 11 Data Saturation Flag (0 valid data, 1 saturated data) |

```

#### Surface Reflectance Aerosol Band 

```{table} Landsat 8 Internal Surface Reflectance Aerosol Quality Assessment Bit Index
:name: table:landsat8-aerosol-index

| Bit | Bit Value | Cumulative Sum | Attribute |
|:-|:-|:-|:-|
| 0 | 1 | 1 | Fill |
| 1 | 2 | 3 | Valid Aerosol Retrieval (center pixel of 3x3 pixel window) |
| 2 | 4 | 7 | Water Pixel (or water pixel was used in the fill-the-window interpolation) |
| 3 | 8 | 15 | Cloud or Cirrus |
| 4 | 16 | 31 | Cloud Shadow |
| 5 | 32 | 63 | Non-center window pixel for which aerosol was interpolated from surrounding 3x3 window center pixels |
| 6-7 | 64 / 128 | 127 / 255 | Aerosol Level<br>00 (0) = Climatology<br>01 (1) = Low<br>10 (2) = Medium<br>11 (3) = High |

```

```{table} Landsat 8 Surface Reflectance Aerosol Values
:name: table:landsat8-aerosol-values

| Attribute | Pixel Value |
|:-|:-|
| Fill | 1 |
| Valid Aerosol Retrieval (center pixel of 3x3 window) | 2,66, 130, 194 |
| Water Pixel (or water pixel was used in the fill-the-window interpolation) | 4, 68, 100, 132, 164, 196, 228 |
| Cloud or Cirrus | 8, 72, 136, 200 |
| Cloud Shadow | 16, 80, 144, 208 |
| Non-center window pixel for which aerosol was interpolated from surrounding 3x3 center pixels | 32, 96, 100, 160, 164, 224, 228 |
| Low-level aerosol | 66, 68, 72, 80, 96, 100 |
| Medium-level aerosol | 130, 132, 136, 144, 160, 164 |
| High-level aerosol | 194, 196, 200, 208, 224, 228 |

```

## Landsat 7

[Landsat 7](https://developers.google.com/earth-engine/datasets/catalog/landsat-7) collection.

### Surface Reflectance

* USGS Landsat 7 Surface Reflectance Tier 1
* USGS Landsat 7 Surface Reflectance Tier 2

### Top of Atmosphere (TOA)

* USGS Landsat 7 Collection 1 Tier 1 TOA Reflectance
* USGS Landsat 7 Collection 1 Tier 1 and Real-Time data TOA Reflectance
* USGS Landsat 7 Collection 1 Tier 2 TOA Reflectance

### Raw Images

* USGS Landsat 7 Collection 1 Tier 1 Raw Scenes
* USGS Landsat 7 Collection 1 Tier 1 and Real-Time data Raw Scenes
* USGS Landsat 7 Collection 1 Tier 2 Raw Scenes

### Derived Datasets

* Burned Area Index (BAI)
* Enhanced Vegetation Index (EVI)
* Normalized Difference Vegetation Index (NDVI)
* Normalized Burn Ratio Thermal (NBRT)
* Normalized Difference Snow Index (NDSI)
* Normalized Difference Water Index (NDWI)

### Specifications and Quality

Section 5 of the Landsat 4-7 Collection 1 (C1) Surface Reflectance  Landsat Ecosystem Disturbance Adaptive Processing System (LEDAPS) [product guide](https://prd-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/atoms/files/LSDS-1370_L4-7_C1-SurfaceReflectance-LEDAPS_ProductGuide-v3.pdf) provides information related to the SR specifications as well to the data quality measurements.

#### Surface Reflectance Specifications

```{table} Landsat 4-7 Surface Reflectance Specifications
:name: table:landsat4to7-sr-specs

| Band Designation     | Band Name                      | Data Type               | Units       | Range         | Valid Range | Fill Value | Saturate Value | Scale Factor |
| :------------------- | :----------------------------- | :---------------------- | :---------- | :-------------  | :----------- |  :---------- | :--------------- | :------------- |
| ProductID_sr_band1   | Band 1                         | 16-Bit Signed Integer   | Reflectance | -2000 - 16000 | 0 - 10000   | -9999      | 20000          | 0.0001       |
| ProductID_sr_band2   | Band 2                         | 16-Bit Signed Integer   | Reflectance | -2000 - 16000 | 0 - 10000   | -9999      | 20000          | 0.0001       |
| ProductID_sr_band3   | Band 3                         | 16-Bit Signed Integer   | Reflectance | -2000 - 16000 | 0 - 10000   | -9999      | 20000          | 0.0001       |
| ProductID_sr_band4   | Band 4                         | 16-Bit Signed Integer   | Reflectance | -2000 - 16000 | 0 - 10000   | -9999      | 20000          | 0.0001       |
| ProductID_sr_band5   | Band 5                         | 16-Bit Signed Integer   | Reflectance | -2000 - 16000 | 0 - 10000   | -9999      | 20000          | 0.0001       |
| ProductID_sr_band6   | Band 6                         | 16-Bit Signed Integer   | Reflectance | -2000 - 16000 | 0 - 10000   | -9999      | 20000          | 0.0001       |
| ProductID_sr_band7   | Band 7                         | 16-Bit Signed Integer   | Reflectance | -2000 - 16000 | 0 - 10000   | -9999      | 20000          | 0.0001       |
| ProductID_sr_atmos_opacity | Atmospheric Opacity | 16-Bit Signed Integer | Unitless | -2000 - 16000 | 0 - 10000 | -9999 | NA | 0.0010 |
| ProductID_pixel_qa   | Level 2 Quality Band           | 16-Bit Unsigned Integer | Bit Index   | 0 - 32768     | 0 - 32768   | 1 (Bit 0)  | NA             | NA           |
| ProductID_radsat_qa  | Radiometric Saturation QA      | 16-Bit Unsigned Integer | Bit Index   | 0 - 32768     | 0 - 32768   | 1 (Bit 0)  | NA             | NA           |
| ProductID_sr_cloud_qa | Surface Reflectance Cloud QA                     | 8-Bit Unsigned Integer  | Bit Index   | 0 - 255       | 0 - 63     | NA        | NA             | NA           |
| ProductID_MTL.txt    | Level 1 Metadata File          | NA                     | NA          | NA            | NA          | NA         | NA             | NA           |
| ProductID_ANG.txt    | Level 1 Angle Coefficient File | NA                     | NA          | NA            | NA          | NA         | NA             | NA           |

```

#### Surface Reflectance Cloud Quality Assessment Band

```{table} Landsat 4-7 Surface Reflectance Cloud Quality Assessment Bit Index
:name: table:landsat4to7-cloud-qa-index

| Bit | Attribute |
|:-|:-|
| 0 | Dark Dense Vegetation (DDV) |
| 1 | Cloud |
| 2 | Cloud Shadow |
| 3 | Adjacent to Cloud |
| 4 | Snow |
| 5 | Water |
| 6 | Unused |
| 7 | Unused |

```

```{table} Landsat 4-7 Surface Reflectance Cloud Quality Assessment Values
:name: table:landsat4to7-cloud-qa-values

| Attribute | Pixel Value |
|:-|:-|
| DDV | 1, 9 |
| Cloud | 2, 34 |
| Cloud Shadow| 4, 12, 20, 36, 52 |
| Adjacent to Cloud | 8, 12, 24, 40, 56 | 
| Snow | 16, 20, 24, 48, 52, 56 |
| Water | 32, 34, 36, 40, 48, 52, 56 |

```

#### Pixel Quality Assessment Band

```{table} Landsat 4-7 Pixel Quality Assessment Bit Index
:name: table:landsat4to7-pixel-qa-index

| Bit | Bit Value | Cumulative Sum | Attribute |
|:-|:-|:-|:-|
| 0 | 1 | 1 | Fill |
| 1 | 2 | 3 | Clear |
| 2 | 4 | 7 | Water |
| 3 | 8 | 15 | Cloud Shadow |
| 4 | 16 | 31 | Snow|
| 5 | 32 | 63 | Cloud |
| 6-7 | 64 / 128 | 127 / 255 | Cloud Confidence<br>00 (0) = None<br>01 (1) = Low<br>10 (2) = Medium<br>11 (3) = High |
| 8 | 256 | 511 | Unused |
| 9 | 512 |  1023 | Unused |
| 10 | 1024 | 2047 | Unused |
| 11 | 2048 | 4095 | Unused |
| 12 | 4096  | 8191 | Unused |
| 13 | 8192 | 16383 | Unused |
| 14 | 16384 | 32767 | Unused |
| 15 | 32768  | 65535 | Unused |

```

```{table} Landsat 4-7 Pixel Quality Assessment Values
:name: table:landsat4to7-pixel-qa-values

| Attribute | Pixel Value |
|:-|:-|
| Fill | 1 |
| Clear | 66, 130 |
| Water | 68, 132 |
| Cloud Shadow | 72, 136 | 
| Snow/Ice | 80, 112, 144, 176 |
| Cloud | 96, 112, 160, 176, 224 |
| Low Confidence Cloud | 66, 68, 72, 80, 96, 112 |
| Medium Confidence Cloud | 130, 132, 136, 144, 160, 176 |
| High Confidence Cloud | 224 |

```

####  Radiometric Saturation Quality Assessment Band

```{table} Landsat 4-7 Radiometric Saturation Quality Assessment Bit Index
:name: table:landsat4to7-radsat-qa-index

| Bit | Bit Value | Cumulative Sum | Description |
|:-|:-|:-|:-|
| 0 | 1 | 1 | Data Fill Flag (0 valid data, 1 invalid data) |
| 1 | 2 | 3 | Band 1 Data Saturation Flag (0 valid data, 1 saturated data) |
| 2 | 4 | 7 | Band 2 Data Saturation Flag (0 valid data, 1 saturated data) |
| 3 | 8 | 15 | Band 3 Data Saturation Flag (0 valid data, 1 saturated data) |
| 4 | 16 | 31 | Band 4 Data Saturation Flag (0 valid data, 1 saturated data) |
| 5 | 32 | 63 | Band 5 Data Saturation Flag (0 valid data, 1 saturated data) |
| 6 | 64 | 127 | Band 6 Data Saturation Flag (0 valid data, 1 saturated data) |
| 7 | 128 | 255 | Band 7 Data Saturation Flag (0 valid data, 1 saturated data) |
| 8 | NA | NA | Not Used |

```

## Landsat 5

[Landsat 5](https://developers.google.com/earth-engine/datasets/catalog/landsat-5) collection.

### Surface Reflectance

* USGS Landsat 5 Surface Reflectance Tier 1
* USGS Landsat 5 Surface Reflectance Tier 2

### Top of Atmosphere (TOA)

* USGS Landsat 5 TM Collection 1 Tier 1 TOA Reflectance
* USGS Landsat 5 TM Collection 1 Tier 2 TOA Reflectance

### Raw Images

* USGS Landsat 5 TM Collection 1 Tier 1 Raw Scenes
* USGS Landsat 5 TM Collection 1 Tier 2 Raw Scenes
* USGS Landsat 5 MSS Collection 1 Tier 1 Raw Scenes
* USGS Landsat 5 MSS Collection 1 Tier 2 Raw Scenes

### Derived Datasets

* Burned Area Index (BAI)
* Enhanced Vegetation Index (EVI)
* Normalized Difference Vegetation Index (NDVI)
* Normalized Burn Ratio Thermal (NBRT)
* Normalized Difference Snow Index (NDSI)
* Normalized Difference Water Index (NDWI)

## Landsat 4

[Landsat 4](https://developers.google.com/earth-engine/datasets/catalog/landsat-4) collection.

### Surface Reflectance

* USGS Landsat 4 Surface Reflectance Tier 1
* USGS Landsat 4 Surface Reflectance Tier 2

### Top of Atmosphere (TOA)

* USGS Landsat 4 TM Collection 1 Tier 1 TOA Reflectance
* USGS Landsat 4 TM Collection 1 Tier 2 TOA Reflectance

### Raw Images

* USGS Landsat 4 TM Collection 1 Tier 1 Raw Scenes
* USGS Landsat 4 TM Collection 1 Tier 2 Raw Scenes
* USGS Landsat 4 MSS Collection 1 Tier 1 Raw Scenes
* USGS Landsat 4 MSS Collection 1 Tier 2 Raw Scenes

### Derived Datasets

* Burned Area Index (BAI)
* Enhanced Vegetation Index (EVI)
* Normalized Difference Vegetation Index (NDVI)
* Normalized Burn Ratio Thermal (NBRT)
* Normalized Difference Snow Index (NDSI)
* Normalized Difference Water Index (NDWI)


## Landsat Multispectral Scanner (MSS) 1-5

[MSS](https://developers.google.com/earth-engine/datasets/catalog/landsat-mss) collections.

### Raw Images

* USGS Landsat 1 MSS Collection 1 Tier 1 Raw Scenes
* USGS Landsat 1 MSS Collection 1 Tier 2 Raw Scenes
* USGS Landsat 2 MSS Collection 1 Tier 1 Raw Scenes
* USGS Landsat 2 MSS Collection 1 Tier 2 Raw Scenes
* USGS Landsat 3 MSS Collection 1 Tier 1 Raw Scenes
* USGS Landsat 3 MSS Collection 1 Tier 2 Raw Scenes
* USGS Landsat 4 MSS Collection 1 Tier 1 Raw Scenes
* USGS Landsat 4 MSS Collection 1 Tier 2 Raw Scenes
* USGS Landsat 5 MSS Collection 1 Tier 1 Raw Scenes
* USGS Landsat 5 MSS Collection 1 Tier 2 Raw Scenes

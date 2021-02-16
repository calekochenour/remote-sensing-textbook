# Chapter 2: Sentinel Collections

[Sentinel](https://developers.google.com/earth-engine/datasets/catalog/sentinel) platform.

## Sentinel-1

[Sentinel-1](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD) collection.

Short name: Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar

* Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground Range Detected, log scaling

## Sentinel-2

[Sentinel-2](https://developers.google.com/earth-engine/datasets/catalog/sentinel-2) collection.

Short name: Sentinel-2 MSI: Multispectral Instrument 

* Sentinel-2 MSI: MultiSpectral Instrument, Level-2A
* Sentinel-2 MSI: MultiSpectral Instrument, Level-1C

### Specifications and Quality

The Sentinel-2 MSI [user guide](https://sentinel.esa.int/web/sentinel/user-guides/sentinel%202-msi), [user handbook](https://sentinel.esa.int/documents/247904/685211/Sentinel-2_User_Handbook.pdf/8869acdf-fd84-43ec-ae8c-3e80a436a16c?t=1438278087000), and [technical guide](https://sentinel.esa.int/web/sentinel/technical-guides/sentinel-2-msi) provide overview of the products and algorithms within the platform. 

Specific to the Level-2A processing, the [Level-2 Algorithm Overview](https://sentinel.esa.int/web/sentinel/technical-guides/sentinel-2-msi/level-2a/algorithm) provides additional information about Scene Classification (SC) and Atmospheric Correction (S2A2).

The Sentinel-2 MSI [data quality reports (DQRs)](https://sentinel.esa.int/web/sentinel/data-product-quality-reports) provide regular updates about the geometric and radiometric performance of the data products.

#### Scene Classification Band

```{table} Sentinel-2 MSI Scene Classification Values
:name: table:sentinel2-sc-values

| Value | Classification |
|:-|:-|
| 0 | No Data |
| 1 | Saturated or Defective |
| 2 | Dark Area Pixels |
| 3 | Cloud Shadows |
| 4 | Vegetation |
| 5 | Not Vegetated |
| 6 | Water |
| 7 | Unclassified |
| 8 | Medium Probability Cloud |
| 9 | High Probability Cloud |
| 10 | Thin Cirrus |
| 11 | Snow |

```

#### Quality Bands

```{table} Sentinel-2 MSI Quality Bands
:name: table:sentinel2-quality-bands

| Band | Description |
|:-|:-|
| MSK_CLDPRB | Cloud Probability Map|
| MSK_SNWPRB | Snow Probability Map |
| QA60 | Cloud Mask |

```

```{table} Sentinel-2 MSI Cloud Mask Bit Index
:name: table:sentinel2-cloud-mask-index

| Bit | Attribute |
|:-|:-|
| 10 | Opaque Clouds<br>0 = No Opaque Clouds<br>1 = Opaque Clouds |
| 11 | Cirrus Clouds<br>0 = No Cirrus Clouds<br>1 = Cirrus Clouds |
        
```


## Sentinel-3

[Sentinel-3](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S3_OLCI) collection.

Short name: Sentinel-3 OLCI EFR: Ocean and Land Color Instrument 

* Sentinel-3 OLCI EFR: Ocean and Land Color Instrument Earth Observation Full Resolution

## Sentinel-5P

[Sentinel-5P](https://developers.google.com/earth-engine/datasets/catalog/sentinel-5p) collection.

Short name: Sentinel-5P TROPOMI: TROPOspheric Monitoring Instrument 

* Sentinel-5P OFFL AER AI: Offline UV Aerosol Index
* Sentinel-5P OFFL CLOUD: Near Real-Time Cloud
* Sentinel-5P OFFL CO: Offline Carbon Monoxide
* Sentinel-5P OFFL HCHO: Offline Formaldehyde
* Sentinel-5P OFFL NO2: Offline Nitrogen Dioxide
* Sentinel-5P OFFL O3: Offline Ozone
* Sentinel-5P OFFL SO2: Offline Sulphur Dioxide
* Sentinel-5P OFFL CH4: Offline Methane
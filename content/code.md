# Code Snippets

```{code-block} python
# Imports
import ee

# Authenticate to GEE; initialze Python API
try:
    ee.Initialize()
except Exception as e:
    ee.Authenticate()
    ee.Initialize()
```

```{code-block} javascript
// Activity 1 - Qualitative Change Detection

// =================================
// Data Acquisition & Pre-Processing
// =================================

// Define boundary for Rocky Mountain National Park, Colorado
var rmnp_boundary = ee.FeatureCollection("users/calekochenour/Rocky_Mountain_National_Park__Boundary_Polygon");

// Define Landsat 8 collection
var landsat8_t1_sr = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR');

// Filter Landsat 8 Tier 1 SR to snow-on conditions near RMNP, 2018
var co_snow_on_2018 = landsat8_t1_sr
  .filterDate('2018-03-01', '2018-04-30')
  .filterBounds(rmnp_boundary)
  .sort('CLOUD_COVER')
  .first();

// Filter Landsat 8 Tier 1 SR to snow-off conditions near RMNP, 2018
var co_snow_off_2018 = landsat8_t1_sr
  .filterDate('2018-07-01', '2018-08-31')
  .filterBounds(rmnp_boundary)
  .sort('CLOUD_COVER')
  .first();

// ===============
// Data Processing
// ===============

// No data processsing in this lab.


// ==================
// Data Visualization
// ==================

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

// Define RMNP boundary visualization parameters
var empty = ee.Image().byte();

var rmnp_boundary_vis = empty.paint({
  featureCollection: rmnp_boundary,
  color: 1,
  width: 3
});

// Center map to Rocky Mountain National Park, Colorado
Map.setCenter(-105.6836, 40.3428, 10);

// Add snow-on and snow-off images to map, RGB and CIR
Map.addLayer(
  rmnp_snow_on_2018,
  l8_vis_params_rgb,
  'Landsat 8 - RGB - 2018 - RMNP - Snow On');

Map.addLayer(
  rmnp_snow_on_2018,
  l8_vis_params_cir,
  'Landsat 8 - CIR - 2018 - RMNP - Snow On');

Map.addLayer(
  rmnp_snow_off_2018,
  l8_vis_params_rgb,
  'Landsat 8 - RGB - 2018 - RMNP - Snow Off');

Map.addLayer(
  rmnp_snow_off_2018,
  l8_vis_params_cir,
  'Landsat 8 - CIR - 2018 - RMNP - Snow Off');

// Add RMNP boundary to map
Map.addLayer(
  rmnp_boundary_vis,
  {'palette': 'FF0000'},
  'RMNP Boundary');


// ===========
// Data Export
// ===========

// No data export in this lab.
```

```{code-block} python
---
lineno-start: 10
emphasize-lines: 1, 3
caption: |
    This is my
    multi-line caption. It is *pretty nifty* ;-)
---
a = 2
print('my 1st line')
print(f'my {a}nd line')
```

```{code-block} ipython
---
class: hide-output
---
print("Hello")
```

```{code-block} ipython
print("Hello")
```

```{code-block} python
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

import quantecon as qe
from numba import njit, jitclass, float64, prange
```

```{code-block} python
f_vals, l_vals = qe.lorenz_curve(w)

fig, ax = plt.subplots()
ax.plot(f_vals, l_vals, label='Lorenz curve, lognormal sample')
ax.plot(f_vals, f_vals, label='Lorenz curve, equality')
ax.legend()
plt.show()
```

```{code-block} ipython
f_vals, l_vals = qe.lorenz_curve(w)

fig, ax = plt.subplots()
ax.plot(f_vals, l_vals, label='Lorenz curve, lognormal sample')
ax.plot(f_vals, f_vals, label='Lorenz curve, equality')
ax.legend()
plt.show()
```


```{math}
---
label: eqn:ndvi
---
ndvi = \frac{nir - red}{nir + red}
```

$$
  ndvi = \frac{nir - red}{nir + red}
$$ (eqn:ndvi_2)

Look at the formula for ndvi: {eq}`eqn:ndvi`

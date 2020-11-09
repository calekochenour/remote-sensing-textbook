# Introduction

This book provides text and examples for how to use [Google Earth Engine](https://earthengine.google.com/) to work through the remote sensing data workflow:

* Acquisition and Preprocessing;
* Processing;
* Postprocessing;
* Visualization; and,
* Export.

The book includes code in `JavaScript` and `Python` languages for completing remote sensing analyses.

Part 1 (beginner) provides introductory modules and activities to introduce Earth Engine functionality. Each example show a few tasks and processes to familiarize the reader with the Earth Engine platform and syntax.

Part 2 (intermediate) provides workflows that piece together tasks and processes from Part 2 in order to create more complex and meaningful workflows, and introduces more complex tasks and processes.

Part 3 (advanced) provides full scientific workflows in Earth Engine that have been re-created from existing, peer-reviewed papers and/or ongoing remote sensing projects. One of the goals of this book it to promote and provide open and reproducible science workflows, and this chapter is dedicated to creating this type of workflow within the Earth Engine platform.



```{toctree}
:hidden:
:titlesonly:
:caption: Beginner Workflows

01-beginner/chapter01-qualitative-change-detection
01-beginner/chapter02-normalized-difference
01-beginner/chapter03-image-composites
01-beginner/chapter04-image-mosaics
01-beginner/chapter05-image-collection-iteration
01-beginner/chapter06-cloud-masking
01-beginner/chapter07-data-quality-bitmasks
```


```{toctree}
:hidden:
:titlesonly:
:caption: Intermediate Workflows

02-intermediate/chapter08-raster-reprojection-resampling
02-intermediate/chapter09-raster-reduce-resolution
02-intermediate/chapter10-spectral-indices-math
02-intermediate/chapter11-image-region-statistics
02-intermediate/chapter12-image-statistics-module
02-intermediate/chapter13-data-correlation
02-intermediate/chapter14-arrays-tasseled-cap
02-intermediate/chapter15-data-conversion-export
```


```{toctree}
:hidden:
:titlesonly:
:caption: Advanced Workflows

03-advanced/chapter16-agriculture-boundaries-vaalharts
03-advanced/chapter17-rice-fields-columbia
03-advanced/chapter18-alpine-treeline-colorado
```

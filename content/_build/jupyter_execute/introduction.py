# Introduction

This book provides text and examples for how to use Google Earth Engine {cite}`gorelick2017google` to work through the remote sensing data workflow:

* Acquisition and Preprocessing;
* Processing;
* Postprocessing;
* Visualization; and,
* Export.

The book includes code in `JavaScript` and `Python` languages for completing remote sensing analyses.

## Content

This book is organized into three parts, with each part containing chapters of higher complexity and longer workflows than the previous part(s). 

### Part 1: Beginner Workflows

Part 1 provides introductory workflows to introduce Earth Engine functionality. Each chapter shows a few tasks and processes to familiarize the reader with the Earth Engine platform and syntax. Part 1 contains Chapters 1-7.

{doc}`Chapter 1 <./01-beginner/chapter01-qualitative-change-detection>` provides a workflow to observe qualitative change from snow-on to snow-off conditions in Rocky Mountain National Park, Colorado, United States. 

{doc}`Chapter 2 <./01-beginner/chapter02-normalized-difference>` provides a workflow to demonstrate the Normalized Difference Vegetation Index (NDVI) for snow-on and snow-off conditions in Rocky Mountain National Park, Colorado, United States.

{doc}`Chapter 3 <./01-beginner/chapter03-image-composites>` provides a workflow to create composite images from a collection of Summer imagery in Rocky Mountain National Park, Colorado, United States.

{doc}`Chapter 4 <./01-beginner/chapter04-image-mosaics>` provides a workflow to create a mosaic image from water features and imagery in Vermont, United States.

{doc}`Chapter 5 <./01-beginner/chapter05-image-collection-iteration>` provides a workflow to iterate through an image collection and calculate the cumulative NDVI difference for imagery in Rocky Mountain National Park, Colorado, United States. 

{doc}`Chapter 6 <./01-beginner/chapter06-cloud-masking>` provides a workflow to mask clouds and cloud shadows within imagery for Rocky Mountain National Park, Colorado, United States.

{doc}`Chapter 7 <./01-beginner/chapter07-data-quality-bitmasks>` provides a workflow to explore quality flag bitmasks for imagery in Rocky Mountain National Park, Colorado, United States.

Chapter quick reference:

* {doc}`./01-beginner/chapter01-qualitative-change-detection`
* {doc}`./01-beginner/chapter02-normalized-difference`
* {doc}`./01-beginner/chapter03-image-composites`
* {doc}`./01-beginner/chapter04-image-mosaics`
* {doc}`./01-beginner/chapter05-image-collection-iteration`
* {doc}`./01-beginner/chapter06-cloud-masking`
* {doc}`./01-beginner/chapter07-data-quality-bitmasks`

### Part 2: Intermediate Workflows 

Part 2 provides workflows that piece together tasks and processes from Part 1 in order to create more complex and meaningful workflows, and introduces more complex tasks and processes.

### Part 3: Advanced Workflows

Part 3 provides full scientific workflows in Earth Engine that have been re-created from existing, peer-reviewed papers and/or ongoing remote sensing projects. One of the goals of this book is to promote and provide open and reproducible science workflows, and this chapter is dedicated to creating this type of workflow within the Earth Engine platform.

## Prerequisites

In order to reproduce the computational workflows in this book, you must have an active [Google Earth Engine account](https://earthengine.google.com/).


## Bibliography

```{bibliography} references.bib
:style: plain
```


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

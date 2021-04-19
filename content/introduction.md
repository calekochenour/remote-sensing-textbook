# Introduction

Imagery is arguably one of the most important and useful geospatial data layers available today; however, it is still one of the most difficult to deploy effectively over the myriad of computing platforms available to geographic information system (GIS) users. The public now takes for granted their ability to see current aerial views of any location on the plant. There are many, many web services and applications that make use of imagery as an interactive backdrop for both the casual and expert user.

Geospatial professionals also want to make use of imagery and other very large raster datasets in an analysis framework. They want to do more than simply view, zoom, pan, and rotate into 3D views. They want to run image processing and analysis algorithms to extract information and features to be used in scientific research, modeling, and decision support systems.

Google Earth Engine (GEE) is an example of a cloud-based image service that combines an extensive archive of satellite imagery, historical and current, with application programming interfaces (APIs) that allow analysis to be performed on this imagery without having to move it to the user's desktop. Noel Gorelick {cite}`gorelick2017google` has written a very nice review of the GEE program and its goals.

Our goal with this online "textbook" resource is to provide example workflows, in both `Javascript` and `Python` that will enable the "student" of GEE to rapidly get up to speed and produce results. We follow a generalized workflow for most image processing tasks that includes the following steps:

* Acquisition and Preprocessing;
* Processing;
* Postprocessing;
* Visualization; and,
* Export.

## Content

This textbook is organized into six parts, with each part containing chapters. Code for all workflows can be found in this GEE [repository](https://code.earthengine.google.com/?accept_repo=users/calekochenour/textbook-activities). The chapter numbers in this textbook match the code in GEE (e.g., Chapter 7: Qualitative Change Detection in the textbook maps to the chapter07-qualitative-change-detection script in GEE).

### Part 1: Data Catalog

Part 1 introduces the imagery collections in the [Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets). Part 1 contains Chapters 1-4.

{doc}`Chapter 1 <./01-catalog/chapter01-landsat>` provides an overview of the Landsat collections and relevant quality information necessary for using the imagery.

{doc}`Chapter 2 <./01-catalog/chapter02-sentinel>` provides an overview of the Landsat collections and relevant quality information necessary for using the imagery.

{doc}`Chapter 3 <./01-catalog/chapter03-modis>` provides an overview of the MODIS collections and products.

{doc}`Chapter 4 <./01-catalog/chapter04-high-resolution>` provides an overview of the high-resolution collections.

### Part 2: Workflow Strategies

Part 2 introduces best practices for remote sensing workflows. Part 2 contains Chapters 5-6.

{doc}`Chapter 5 <./02-strategies/chapter05-preprocessing-tasks>` provides an introduction to imagery preprocessing tasks.

{doc}`Chapter 6 <./02-strategies/chapter06-tips-and-tricks>` provides useful (and possibly lesser known) tips and tricks.

### Part 3: Beginner Workflows

Part 3 provides introductory workflows to introduce Earth Engine functionality. Each chapter shows a few tasks and processes to familiarize the reader with the Earth Engine platform and syntax. Part 3 contains Chapters 7-15.

{doc}`Chapter 7 <./03-beginner/chapter07-qualitative-change-detection>` provides a workflow to observe qualitative change from snow-on to snow-off conditions in Rocky Mountain National Park, Colorado, United States.

{doc}`Chapter 8 <./03-beginner/chapter08-normalized-difference-vegetation-index>` provides a workflow to demonstrate the Normalized Difference Vegetation Index (NDVI) for snow-on and snow-off conditions in Rocky Mountain National Park, Colorado, United States.

{doc}`Chapter 9 <./03-beginner/chapter09-image-composites>` provides a workflow to create composite images from a collection of Summer imagery in Rocky Mountain National Park, Colorado, United States.

{doc}`Chapter 10 <./03-beginner/chapter10-image-mosaics>` provides a workflow to create a mosaic image from water features and imagery in Vermont, United States.

{doc}`Chapter 11 <./03-beginner/chapter11-image-collection-iteration>` provides a workflow to iterate through an image collection and calculate the cumulative NDVI difference for imagery in Rocky Mountain National Park, Colorado, United States.

{doc}`Chapter 12 <./03-beginner/chapter12-cloud-masking>` provides a workflow to mask clouds and cloud shadows within imagery for Rocky Mountain National Park, Colorado, United States.

{doc}`Chapter 13 <./03-beginner/chapter13-data-quality-bitmasks>` provides a workflow to explore quality flag bitmasks for imagery in Rocky Mountain National Park, Colorado, United States.

{doc}`Chapter 14 <./03-beginner/chapter14-image-to-asset>` provides a workflow to export an image to a GEE Asset.

{doc}`Chapter 15 <./03-beginner/chapter15-image-band-histograms>` provides a workflow to explore image band histograms for an area near Lake Champlain and Burlington, Vermont, United States.

### Part 4: Intermediate Workflows

Part 4 provides workflows that piece together tasks and processes from Part 2 in order to create more complex and meaningful workflows, and introduces more complex tasks and processes. Part 4 contains Chapters 16-24.

{doc}`Chapter 16 <./04-intermediate/chapter16-raster-reprojection-resampling>` provides a workflow to reproject and resample imagery for an area near Manchester, Vermont, United States.

{doc}`Chapter 17 <./04-intermediate/chapter17-raster-reduce-resolution>` provides a workflow to reduce the resolution of imagery for an area near Manchester, Vermont, United States.

{doc}`Chapter 18 <./04-intermediate/chapter18-spectral-indices-math>` provides a workflow to create spectral indices for Rocky Mountain National Park, Colorado, United States.

{doc}`Chapter 19 <./04-intermediate/chapter19-image-region-statistics>` provides a workflow to create image statistics for an Ecoregion in United States High Plains.

{doc}`Chapter 20 <./04-intermediate/chapter20-image-statistics-module>` provides a module containing common functions for image statistics.

{doc}`Chapter 21 <./04-intermediate/chapter21-data-correlation>` provides a workflow to explore data correlation between vegetation and terrain in the Gabilan Range, California, United States.

{doc}`Chapter 22 <./04-intermediate/chapter22-arrays-tasseled-cap>` provides a workflow to explore arrays and the Tasseled Cap transformation for an area near Lake Champlain, Vermont, United States.

{doc}`Chapter 23 <./04-intermediate/chapter23-data-conversion-export>` provides a workflow to convert raster features to vector and export both raster and vector features for Rocky Mountain National Park, Colorado, United States.

{doc}`Chapter 24 <./04-intermediate/chapter24-image-collection-export>` provides a workflow to export all images in a collection from June 1, 2020 to January 21, 2021 for Rocky Mountain National Park, Colorado, United States.

### Part 5: Advanced Workflows

Part 5 provides full scientific workflows in Earth Engine that have been re-created from existing, peer-reviewed papers and/or ongoing remote sensing projects. One of the goals of this book is to promote and provide open and reproducible science workflows, and this chapter is dedicated to creating this type of workflow within the Earth Engine platform. Part 5 contains Chapters 25-27.

{doc}`Chapter 25 <./05-advanced/chapter25-agriculture-boundaries-vaalharts>` provides a partial implementation of Watkins and van Niekerk {cite}`WATKINS2019294` to delineate agriculture field boundaries in the Vaalharts Irrigation Scheme, South Africa.

{doc}`Chapter 26 <./05-advanced/chapter26-rice-fields-columbia>` provides a workflow to identify rice fields based on change detection in the Tolima Department, Columbia.

{doc}`Chapter 27 <./05-advanced/chapter25-agriculture-boundaries-vaalharts>` provides a partial implementation of Wei, Karger, and Wilson {cite}`WEI2020111672` (applied to Rocky Mountain National Park, Colorado, United States) to map the alpine treeline ecotone.

### Part 6: Appendices

Part 6 provides supplemental information in the form of appendices. Current appendices include: Part 6 contains Appendices A-B.

{doc}`Appendix A <./06-appendices/appendix-a-acronym-list>` provides a list of acronyms used in this textbook.

{doc}`Appendix B <./06-appendices/appendix-b-bibliography>` provides a list of citations used in this textbook.

## Prerequisites

In order to reproduce the computational workflows in this book, you must have an active [Google Earth Engine account](https://earthengine.google.com/).

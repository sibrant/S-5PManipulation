# S-5PManipulation

This set of scripts was developed as a short research project for the 1st ESA Atmospheric Training course, held in Cluj, Romania in November 2019. Resulting image is a animated GIFF of Sentinel-5P Absored Aerosol Index data over Australia between December 2019 and January 2020.

The idea of this project was to showcase processing capabilities on the CREODIAS cloud computing platform. It searches the CREODIAS data repository through their Finder API, collects the Sentinel-5P AAI data, pre-processes with HARP tools and creates daily GeoTIFF files. These files can subsequently be converted into an animated GIFF.

The script runs from a VM on CREODIASd. Alternatively, the data could be queried and downloaded prior to the analysis, but that would 

The Python script S5p_query_proc.py searches the CREODIAS repository for Sentinel-5P data and pre-processes the returned data to daily GeoTIFFs.

The R script S5p_giff.R creates an animated GIFF of the pre-processed GeoTIFFs.

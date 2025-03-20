# AALU_ Workshop: Map Points to Tiles
:earth_asia: :computer:

<img width="1728" alt="Screenshot 2025-03-20 at 8 08 26 PM" src="https://github.com/user-attachments/assets/febd9f2d-2a0c-42cb-bdc8-9805465bef84" />


## Introduction
This workshop provides an introduction to the Google Static Maps API, a powerful tool for downloading satellite and aerial imagery via a straightforward Python script. The script serves as an entry point into visual research, allowing to explore a chosen topic by gathering and scraping point locations from various APIs.

An API, or Application Programming Interface, is a set of rules and tools that allows different software applications to communicate with each other. Think of it like a waiter in a restaurant: the waiter is the intermediary that takes your order (your request for information or action), brings it to the kitchen (a software system), and then brings the food (the data or outcome) back to you.

Goal of the workshop is to transform the points gathered through API into tiles and arrange them in a grid or video format, ultimately merging them to create a alternative narratives of geospatial data.

The goal of the workshop is to transform points gathered through APIs into tiles and arrange them in a grid or video format, creating alternative narratives of geospatial data. At the end of the day everyone will get a starting/basic knowledge of APIs and Python through very simple codes, in order to download satellite images based on latitude and longitude coordinates provided in a CSV file. Unlike the georeferenced multispectral satellite data from Landsat or Sentinel, the imagery retrieved in this workshop lacks embedded geographic metadata and is not suitable for georeferencing, making it ideal for a more non-GIS use and experiments.

The workflow for the session is as follows:

<img width="597" alt="Screenshot 2025-03-20 at 6 24 24 PM" src="https://github.com/user-attachments/assets/f54b4f84-af30-40a6-91b9-d84ca759beae" />


The outcome of the workshop is imagined to be a collection of non-georeferenced.png image files. These images are perfect for assembling into visual arrays and animations that are designed for use outside of traditional GIS software, and each group can decide to layer them in a "screen performance" according to their creativity.



## Setup Requirements
- ### Google Maps API
   - Before you begin, follow the steps provided [here](https://developers.google.com/maps/documentation/maps-static/start) to obtain a Google API key for the Static Maps API. It's crucial to activate billing for your API key to use the script, though you will not face any charges for the project scope described in this tutorial. Google generously offers $200 in monthly credits for each API account, which equates to downloading approximately 100,000 images from the Static Maps API each month at no cost. For detailed information on API pricing, refer to this page.
It is IMPORTANT to keep your API key confidential. Exposure of your key could potentially lead to substantial unauthorized charges. This tutorial does not require sharing the code externally, so security concerns are minimized for this exercise.

- ### Visual Studio Code
   - Download Visual Studio Code [here](https://code.visualstudio.com/).

- ### QGIS
   - QGIS is an open-source GIS platform. Download it from [here](https://www.qgis.org/en/site/).

- ### GitHub
   - Set up a GitHub account [here](https://github.com/) to manage and share your project code.

### Python
#### For macOS
- Download Python from the [Python downloads page for macOS](https://www.python.org/downloads/macos/).
- Install Homebrew by pasting the following in Terminal: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- Install Python via Homebrew: `brew install python`
- Verify installation with: `python3 --version`

#### For Windows
- Download Python from the [Python downloads page for Windows](https://www.python.org/downloads/windows/).
- During installation, check "Add Python 3.x to PATH".
- Follow installation prompts.

## How to Get Data
### Data Acquisition Techniques
- **OpenStreetMap (OSM)**: Use OSM for a starting point to understand geographical locations.
- **Overpass API**: Customize queries to fetch detailed information from OSM, which can then be imported into QGIS.

#### Example Query
```query
[out:json][timeout:25];
(
  node["amenity"="school"]({{bbox}});
  way["amenity"="school"]({{bbox}});
  relation["amenity"="school"]({{bbox}});
);
out body;
>;
out skel qt;


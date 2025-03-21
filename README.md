# AALU_ Workshop: Map Points to Tiles
:earth_asia: :computer:

<img width="1728" alt="Screenshot 2025-03-20 at 8 08 26 PM" src="https://github.com/user-attachments/assets/febd9f2d-2a0c-42cb-bdc8-9805465bef84" />


## Introduction
This workshop provides an introduction to the Google Static Maps API, a powerful tool for downloading satellite and aerial imagery via a straightforward Python script. The script serves as an entry point into visual research, allowing to explore a chosen topic by gathering and scraping point locations from various APIs.

An API, or Application Programming Interface, is a set of rules and tools that allows different software applications to communicate with each other. Think of it like a waiter in a restaurant: the waiter is the intermediary that takes your order (your request for information or action), brings it to the kitchen (a software system), and then brings the food (the data or outcome) back to you.

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
   - or use Terminal
      - Install Homebrew by pasting the following in *Terminal*: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
      - Install Python via Homebrew: `brew install python`
      - Verify installation with: `python3 --version`

#### For Windows
- Download Python from the [Python downloads page for Windows](https://www.python.org/downloads/windows/).
- During installation, check "Add Python 3.x to PATH".
- Follow installation prompts.

  
#### errors: 
If you get any errors it's likely you miss the dependencies run the code below in your Terminal inside Visual Studio Code:
pip install requests moviepy

## HOW TO GET DATA:

### OpenStreetMap (OSM) 
- **OpenStreetMap (OSM)**: OpenStreetMap (OSM) is a dynamic, collaborative project to build a freely editable map of the world. It serves as an excellent source of geospatial data, enriched by a global community of mappers. The open-source nature of OSM means that while the data is rich and diverse, its accuracy and detail can vary, thus it shouldn't be solely relied upon for critical data needs. For our workshop, OSM is a valuable starting point to understand geographical locations and examine landforms.
  
- **Overpass API**: To delve deeper and extract specific features or points based on tailored criteria, we use the [Overpass API](https://overpass-turbo.eu/). This powerful tool enables the definition of custom queries to fetch detailed information from OSM, which can then be directly imported into QGIS for enriched analysis.
     - For example, if you're interested in mapping specific amenities, like schools, you might structure your Overpass API query as follows:

#### Example Query 1
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
```

To adapt this query for different features, simply change the "amenity"="school" parameter to your feature of interest. You can find a complete list of mappable features on the [OSM Wiki: Map Features](https://wiki.openstreetmap.org/wiki/Map_features).
    - Changing the Feature Type (Tag): The amenity=school part of the query is a tag filter (amenity is the key, and school is the value). To change the feature you're interested in, replace school with another value. For example:
        - To find prisons: "amenity"="prison"
        - To find hospitals: "amenity"="hospital"
   - Choosing Node, Way, or Relation: Decide whether to use node, way, or relation based on the type of feature you are interested in:
     1. Node: Use if the feature is typically a point location (e.g., a water well, a bus stop).
     2. Way: Use for linear features (e.g., roads, rivers) or areas (e.g., park perimeters, building footprints).
     3. Relation: Use for complex structured features that can't be adequately represented as a single node or way (e.g., a bus route involving multiple streets, a forest with several disjointed parts).
     
#### Example Query 2
```query

[out:json][timeout:25];
(
  // Retrieve nodes and ways that represent rivers
  node["waterway"="river"]({{bbox}});
  way["waterway"="river"]({{bbox}});
  relation["waterway"="river"]({{bbox}});

  // Retrieve nodes and ways that represent streams
  node["waterway"="stream"]({{bbox}});
  way["waterway"="stream"]({{bbox}});
  relation["waterway"="stream"]({{bbox}});
);
out body;
>;
out skel qt;
```

### Google Maps: Using 'My Maps'
- **Google Maps**: offers a 'My Maps' feature that allows us to trace paths or mark areas, which can be exported in KML format. This format is highly compatible with QGIS, providing a good vector base for extracting points. This tool is particularly useful if your analysis focuses on architectural elements—explore street surroundings and buildings from a human-eye perspective. Using this technique allow togather easily snapshots from Google Street View to have visual analysis with both aerial and street-level views.
  
<img width="1728" alt="Screenshot 2025-03-20 at 8 36 46 PM" src="https://github.com/user-attachments/assets/4feeb1c6-e578-4266-8594-3370ac800850" />

### Trace Geometry/Path in QGIS
- **QGIS**: Building on results from OpenStreetMap or Google Maps—or even starting from scratch—we'll use QGIS to directly draw geometries to explore. This involves creating paths or outlining areas to derive specific coordinate points.

In all three cases, the goal is to compile these coordinates into a CSV file, which can then be used to pull images from Google Maps, whether satellite or street views, generating a diverse range of geographical visualizations.


## HOW TO VISUALIZE DATA AND DEFINE POINTS:

We will work together on QGIS to import data from previous steps, and make a csv point lists.

Some points to remember:
- ALWAYS add new fields for Latitude and Longitude
   - Click on the "Field Calculator" icon.
   - Create a new field named Latitude. Set the type to Decimal number, and use the expression y($geometry) to calculate the latitude.
   - Create another field named Longitude. Set the type to Decimal number, and use the expression x($geometry) to calculate the longitude.
- ALWAYS add new field for Index
    - Click on the “Open Field Calculator” icon. This opens the Field Calculator.
    - Check the Create a new field option.
    - Set the output field name as ID or another name of your choice.
    - Set the field type to Integer.
    - For the Expression, enter: @row_number
    - This expression automatically generates a sequence of numbers starting from 1, assigning each row in your table a unique number.

 - You can use the "Points along geometry" tool to place points along the line, specifying the interval in degrees. This is an atypical use and the results might not be meaningful for distance measurements, but it will provide points at angular intervals:
    - Open the Tool: Go to Vector > Geometry Tools > Points along geometry….
    - Input Layer: Select your line layer.
    - Distance: Enter your desired interval in degrees (note: very small values like 0.001 degrees or similar might be necessary depending on your geographic extent).
    - Output: Choose where to save the output layer - same folder with other files.

- Once exported the CSV file from QGIS, make sure (using excel or google sheet) to have columns in this order: Index, Latitude, Longitude.

<img width="229" alt="Imageexcel" src="https://github.com/user-attachments/assets/52d67a5a-1b3f-459b-84af-dc2addd2f869" />

This will make sure the Python script will be running smoothly with no errors. (hopefully :)))

## RUN PYTHON CODE:

There are two main scripts attached below (and also uploaded here on github satellite.py and street.py): the first is to obtain satellite imagery based on coordinate points, save them as PNGs in a folder, and create a video. The second performs the same process but gathers street view images according to camera angle and focal length, saves the PNGs in a folder, and creates a video.

### Satellite View (satellite.py)


```python
import os
import requests
import csv
from moviepy.editor import ImageSequenceClip

def satellite_squares(csv_file, api_key, zoom=18, size=640, output_folder="satellite_images", fps=5):
    """
    Fetches high-resolution Google Maps satellite images based on coordinates from a CSV file and creates a video from these images.
    
    Parameters:
        csv_file (str): Path to CSV file containing coordinates.
        api_key (str): Google Maps API Key.
        zoom (int): Zoom level for detailed imaging.
        size (int): Image size in pixels (max 640, but scale=4 allows 1280x1280).
        output_folder (str): Directory to save images.
        fps (int): Frames per second in the output video.
    """
    
    base_url = f"https://maps.googleapis.com/maps/api/staticmap?scale=4&size={size}x{size}&maptype=satellite"
    locations = []
    image_files = []

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Read CSV file containing coordinates
    with open(csv_file, 'rt') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                ind, lat, lng = str(row[0]), float(row[1]), float(row[2])
                locations.append((ind, lat, lng))
            except ValueError:
                print(f"Skipping invalid row: {row}")

    # Fetch images for each coordinate
    for ind, lat, lng in locations:
        latlng = f"center={lat},{lng}"
        key_param = f"key={api_key}"
        url = f"{base_url}&zoom={zoom}&{latlng}&{key_param}"
        filename = os.path.join(output_folder, f"{ind}.png")
        image_files.append(filename)

        res = requests.get(url)
        if res.status_code == 200:
            with open(filename, "wb") as file:
                file.write(res.content)
            print(f"Saved: {filename}")
        else:
            print(f"Failed to fetch {ind} ({lat}, {lng}) | HTTP {res.status_code}")

    # Create a video from the images
    if image_files:
        clip = ImageSequenceClip(image_files, fps=fps)
        video_filename = os.path.join(output_folder, "satellite_view_video.mp4")
        clip.write_videofile(video_filename, codec="libx264")
        print(f"Video saved as {video_filename}")

    print("Image fetching complete.")

# Example usage
csv_file_path = "coordinates.csv"  # Your CSV file with IDs and coordinates
api_key = "API-KEY"  # Replace with your API key

satellite_squares(csv_file_path, api_key)
```


### Street View (street.py)
```python
import os
import requests
import csv
from moviepy.editor import ImageSequenceClip

def street_view_images(csv_file, api_key, size="640x640", fov=50, pitch=0, heading=160, output_folder="street_view_images", fps=20):
    """
    Fetches Google Maps Street View images based on coordinates from a CSV file and creates a video from these images.
    
    Parameters:
        csv_file (str): Path to CSV file containing coordinates.
        api_key (str): Google Maps API Key.
        size (str): Image size in pixels (default "640x640").
        fov (int): Field of view of the camera (default 90, range 0-120).
        pitch (int): The up or down angle of the camera relative to the Street View vehicle (default 0, range -90 to 90).
        heading (int): The compass heading of the camera (default 0, range 0-360).
        output_folder (str): Directory to save images.
        fps (int): Frames per second in the output video.
    """
    base_url = "https://maps.googleapis.com/maps/api/streetview"
    locations = []
    image_files = []

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Read CSV file containing coordinates
    with open(csv_file, 'rt') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                ind, lat, lng = str(row[0]), float(row[1]), float(row[2])
                locations.append((ind, lat, lng))
            except ValueError:
                print(f"Skipping invalid row: {row}")

    # Fetch images for each coordinate
    for ind, lat, lng in locations:
        params = {
            'size': size,
            'location': f"{lat},{lng}",
            'fov': fov,
            'pitch': pitch,
            'heading': heading,
            'key': api_key
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            filename = os.path.join(output_folder, f"{ind}.jpg")
            image_files.append(filename)
            with open(filename, 'wb') as image_file:
                image_file.write(response.content)
            print(f"Saved: {filename}")
        else:
            print(f"Failed to fetch {ind} ({lat}, {lng}) | HTTP {response.status_code}")

    # Create a video from the images
    if image_files:
        clip = ImageSequenceClip(image_files, fps=fps)
        clip.write_videofile(os.path.join(output_folder, "street_view_video.mp4"), codec="libx264")

    print("Image fetching complete.")

# Example usage
csv_file_path = "coordinates.csv"  # Your CSV file with IDs and coordinates
api_key = "API-KEY"  # Replace with your API key

street_view_images(csv_file_path, api_key)
```


- **Heading**: This parameter controls the compass heading of the camera. It accepts values from 0 to 360, where 0 or 360 is north, 90 is east, 180 is south, and 270 is west. Adjusting the heading allows you to rotate the camera to face the building directly or from different angles.
- **Pitch**: The pitch adjusts the angle at which the camera points upwards or downwards. The values range from -90 (directly down) to 90 (directly up), with 0 being level with the horizon. To better focus on facades, a slight upward pitch can be beneficial.
- **Field of View (FOV)**: The fov parameter adjusts the zoom level of the camera. It can range from 0 to 120, where lower values zoom in more, narrowing the field of view. Adjusting the FOV can help you get a closer look at architectural details without physically moving the camera location.

## VISUALIZE THE GRID:
Once you are happy with the set of images and want to visualize them all together in a grid to see them as a system, you can download the HTML file called 'index-grid.html' from the GitHub folder. Ensure that the name of the CSV file is correct, the image files are either in .png or .jpg format, and that the file is in the same folder, then run the code.

## MAKE YOUR OWN NARRATIVE:
Once you've collected your grid and potentially a series of videos from different sets of points as an output of this workshop, you can assemble these different forms of media together on your screen. Consider doing a screen recording, using your microphone to walk us through the process as a screen walk. There's no need to be specific; just have fun, whether it's for a couple of seconds or a few minutes!

 


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

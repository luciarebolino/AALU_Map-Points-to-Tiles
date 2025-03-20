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
        zoom (int): Zoom level (default: 18 for high detail).
        size (int): Image size in pixels (max 640, but scale=2 allows 1280x1280).
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
        filename = os.path.join(output_folder, f"{ind}.png")  # Filename now only contains the index number
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
csv_file_path = "test-tutorial-4.csv"  # Your CSV file with IDs and coordinates
api_key = "AIzaSyDTEZeV5GmRFh1-TQm_v8RCxWOGmWaMivM"  # Replace with your API key

satellite_squares(csv_file_path, api_key)

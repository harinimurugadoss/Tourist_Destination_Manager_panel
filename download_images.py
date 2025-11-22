import os
import requests
from pathlib import Path

def download_image(url, filename):
    """Download an image from a URL and save it to the static/images/destinations directory."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Save the image
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

# Define the images to download
images = [
    {"url": "https://source.unsplash.com/1600x600/?taj-mahal,india", "name": "taj-mahal.jpg"},
    {"url": "https://source.unsplash.com/1600x600/?himalayas,mountains", "name": "himalayas.jpg"},
    {"url": "https://source.unsplash.com/1600x600/?goa,beach", "name": "goa-beach.jpg"},
    {"url": "https://source.unsplash.com/600x400/?taj-mahal", "name": "taj-mahal-thumb.jpg"},
    {"url": "https://source.unsplash.com/600x400/?manali,mountains", "name": "manali.jpg"},
    {"url": "https://source.unsplash.com/600x400/?goa,beach", "name": "goa.jpg"}
]

# Download all images
for img in images:
    filename = os.path.join("static", "images", "destinations", img["name"])
    if not os.path.exists(filename):
        download_image(img["url"], filename)
    else:
        print(f"{filename} already exists, skipping...")

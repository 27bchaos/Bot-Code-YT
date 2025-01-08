import os
import time
import subprocess
import requests
from PIL import Image

# Path to your static image
IMAGE_FILE = './static_images.png'  # Replace with your image file path (static image for video)

# Google Drive File ID (replace this with your file ID from Google Drive URL)
google_drive_audio_id = "10Dk1IwOW-p2CTzTkuCc4-JWdD_wRvtwi"  # Replace with your actual Google Drive file ID

# URL to download the audio from Google Drive
audio_url = f"https://drive.google.com/uc?export=download&id={google_drive_audio_id}"

# Replace with your YouTube stream URL and stream key
stream_key = "16ef-abm0-6aat-f5d6-3dv0"  # Replace with your actual stream key
rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

# Directory for temporarily storing the downloaded audio
MUSIC_DIR = './music_files'

# Ensure the music directory exists
if not os.path.exists(MUSIC_DIR):
    os.makedirs(MUSIC_DIR)

# Function to download audio from Google Drive and save it locally
def download_audio(url, file_path):
    print(f"Downloading audio from: {url}")
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete.")
    else:
        print(f"Failed to download audio. Status code: {response.status_code}")

# Function to resize the image to even dimensions for FFmpeg compatibility
def resize_image(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        # Ensure dimensions are even
        new_width = width if width % 2 == 0 else width + 1
        new_height = height if height % 2 == 0 else height + 1
        
        if (new_width, new_height) != (width, height):
            print(f"Resizing image from {width}x{height} to {new_width}x{new_height}")
            img = img.resize((new_width, new_height))
            img.save(image_path)  # Save resized image back to disk
        else:
            print(f"Image already has even dimensions: {width}x{height}")

# Function to stream audio with static image to YouTube via FFmpeg
def stream_audio():
    while True:
        # Define the audio file path
        audio_file_path = os.path.join(MUSIC_DIR, 'song1.mp3')

        # Download the audio file from Google Drive
        download_audio(audio_url, audio_file_path)

        print(f"Selected audio file: song1.mp3")
        print(f"Audio path: {audio_file_path}")

        # Resize image for compatibility with FFmpeg (even dimensions required)
        resize_image(IMAGE_FILE)

        # FFmpeg command to stream audio with static image
        ffmpeg_command = [
            'ffmpeg', 
            '-re',  # Read input at native frame rate
            '-i', audio_file_path,  # Input audio file
            '-loop', '1',  # Loop the image
            '-i', IMAGE_FILE,  # Input static image
            '-c:v', 'libx264',  # Video codec
            '-preset', 'veryfast',  # Encoding preset
            '-c:a', 'aac',  # Audio codec
            '-b:a', '128k',  # Audio bitrate
            '-ar', '44100',  # Set audio sample rate (44.1 kHz)
            '-ac', '2',  # Set number of audio channels (stereo)
            '-f', 'flv',  # Output format
            rtmp_url  # RTMP stream URL
        ]

        print(f"Executing FFmpeg command: {' '.join(ffmpeg_command)}")

        try:
            ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = ffmpeg_process.communicate()

            # Check for errors and log them
            if ffmpeg_process.returncode != 0:
                print(f"FFmpeg Error: {stderr.decode()}")
            else:
                print(f"Successfully started streaming: song1.mp3")
            print(f"FFmpeg Output: {stdout.decode()}")

        except Exception as e:
            print(f"Error while streaming audio: {e}")

        time.sleep(5)  # Pause for 5 seconds before restarting the process

# Start streaming
if __name__ == "__main__":
    print("Starting streaming process...")
    stream_audio()

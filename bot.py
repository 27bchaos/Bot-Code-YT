import os
import time
import subprocess
from PIL import Image

# Path to your static image
IMAGE_FILE = './static_images.png'  # Replace with your image file path (static image for video)

# Audio stream URL (Updated to use your URL)
audio_stream_url = "https://prod-3-84-19-111.amperwave.net/audacy-wqalfmaac-imc"

# Directory for temporarily storing the downloaded audio (if needed)
MUSIC_DIR = './music_files'

# Ensure the music directory exists
if not os.path.exists(MUSIC_DIR):
    os.makedirs(MUSIC_DIR)

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

# Function to stream audio from URL with static image to YouTube via FFmpeg
def stream_audio():
    # Resize image for compatibility with FFmpeg (even dimensions required)
    resize_image(IMAGE_FILE)

    while True:
        # FFmpeg command to stream audio from URL with static image
        ffmpeg_command = [
            'ffmpeg', 
            '-i', audio_stream_url,  # Audio stream URL as input
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
                print(f"Successfully started streaming from: {audio_stream_url}")
            print(f"FFmpeg Output: {stdout.decode()}")

        except Exception as e:
            print(f"Error while streaming audio: {e}")

        time.sleep(5)  # Pause for 5 seconds before restarting the process

# Replace with your YouTube stream URL and stream key
stream_key = "mf0k-vv7a-rcb2-dcwe-az92"  # Replace with your actual stream key
rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

# Start streaming
if __name__ == "__main__":
    print("Starting streaming process...")
    stream_audio()

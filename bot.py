import random
import time
import os
from rtmp import RTMPClient

# Path to your local music files
MUSIC_DIR = './music_files'
IMAGE_FILE = './static_image.png'  # Static image for the video stream

# Get list of audio files
AUDIO_FILES = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav', '.flac'))]

# Stream key from YouTube
stream_key = "m5dp-tt7s-e18e-gze0-3gge"
rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

# Set up the RTMP client
client = RTMPClient(rtmp_url)

# Function to stream audio with image using RTMP
def stream_audio():
    while True:
        audio_file = random.choice(AUDIO_FILES)
        audio_path = os.path.join(MUSIC_DIR, audio_file)

        print(f"Streaming: {audio_file}")

        # Use RTMPClient to stream the content (audio + image)
        client.send_audio_and_video(audio_path, IMAGE_FILE)

        time.sleep(5)  # Sleep before streaming next audio

if __name__ == "__main__":
    stream_audio()

import os
import random
import time
import subprocess
from flask import Flask, Response
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)

# Path to your local music files
MUSIC_DIR = './music_files'  # Replace this with the directory where your music files are stored

# Ensure the music directory exists
if not os.path.isdir(MUSIC_DIR):
    print(f"Error: Music directory {MUSIC_DIR} not found.")
    exit()

# Get list of audio files in the directory
AUDIO_FILES = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav', '.flac'))]

# Ensure there are audio files available to stream
if not AUDIO_FILES:
    print("No music files found in the specified directory.")
    exit()

# YouTube Live Streaming setup (stream URL and stream key)
# Replace 'YOUR_STREAM_KEY' with your actual stream key from YouTube
RTMP_URL = 'rtmp://a.rtmp.youtube.com/live2/'
STREAM_KEY = 'YOUR_STREAM_KEY'  # Replace with your actual stream key from YouTube

# Function to generate and stream audio to YouTube
def generate_audio():
    while True:
        # Randomly select an audio file from the list
        audio_file = random.choice(AUDIO_FILES)
        audio_path = os.path.join(MUSIC_DIR, audio_file)

        print(f"Streaming audio: {audio_file}")

        # Using FFmpeg to stream the selected file to YouTube
        try:
            ffmpeg_process = subprocess.Popen(
                ['ffmpeg', '-re', '-i', audio_path, '-f', 'flv', 
                 f'{RTMP_URL}{STREAM_KEY}'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            # Read the output and error streams from FFmpeg
            stdout, stderr = ffmpeg_process.communicate()

            if stdout:
                print(stdout.decode('utf-8'))
            if stderr:
                print(stderr.decode('utf-8'))
            
        except Exception as e:
            print(f"Error while streaming audio file {audio_file}: {e}")

        time.sleep(5)  # Pause for 5 seconds before switching to the next track

@app.route('/stream')
def stream_audio():
    # Start streaming audio to the YouTube live stream
    return Response(generate_audio(), mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

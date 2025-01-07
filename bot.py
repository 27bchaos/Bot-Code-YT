import os
import random
import time
import subprocess
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask, Response

app = Flask(__name__)

# Path to your local music files
MUSIC_DIR = './music_files'  # Replace this with your directory of music files

# Get list of audio files
AUDIO_FILES = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav', '.flac'))]

# Ensure the music directory exists
if not AUDIO_FILES:
    print("No music files found in the specified directory.")
    exit()

# Function to generate live stream from local files
def generate_audio():
    while True:
        # Randomly select an audio file from the list
        audio_file = random.choice(AUDIO_FILES)
        audio_path = os.path.join(MUSIC_DIR, audio_file)

        print(f"Streaming audio: {audio_file}")

        # Using FFmpeg to stream the selected file
        # Make sure that ffmpeg is installed and properly configured
        try:
            ffmpeg_process = subprocess.Popen(['ffmpeg', '-re', '-i', audio_path, '-f', 'flv', 'rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY'],
                                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_process.communicate()
        except Exception as e:
            print(f"Error while streaming audio file {audio_file}: {e}")

        time.sleep(5)  # Pause for 5 seconds before switching to the next track

@app.route('/stream')
def stream_audio():
    return Response(generate_audio(), mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


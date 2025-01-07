import os
import random
import time
import subprocess
from flask import Flask, Response

app = Flask(__name__)

# Path to your local music files
MUSIC_DIR = './music_files'  # Replace this with your directory of music files
IMAGE_FILE = './static_image.png'  # Replace with your image file path (static image for video)

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

        # Using FFmpeg to stream the selected file with a static image
        try:
            ffmpeg_command = [
                'ffmpeg', 
                '-re',  # Read input at native frame rate
                '-i', audio_path,  # Input audio file
                '-loop', '1',  # Loop the image
                '-i', IMAGE_FILE,  # Input static image
                '-c:v', 'libx264',  # Video codec
                '-preset', 'veryfast',  # Encoding preset
                '-c:a', 'aac',  # Audio codec
                '-b:a', '128k',  # Audio bitrate
                '-f', 'flv',  # Output format
                'rtmp://a.rtmp.youtube.com/live2/m5dp-tt7s-e18e-gze0-3gge'  # Replace with your YouTube stream key
            ]
            # Start the FFmpeg process
            ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = ffmpeg_process.communicate()

            # Check for errors and log them
            if ffmpeg_process.returncode != 0:
                print(f"FFmpeg Error: {stderr.decode()}")
            else:
                print(f"Streaming audio file: {audio_file}")
        except Exception as e:
            print(f"Error while streaming audio file {audio_file}: {e}")

        time.sleep(5)  # Pause for 5 seconds before switching to the next track

@app.route('/stream')
def stream_audio():
    return Response(generate_audio(), mimetype='audio/mpeg')

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)

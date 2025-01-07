import os
import random
import time
import subprocess

# Path to your local music files
MUSIC_DIR = './music_files'  # Replace this with your directory of music files
IMAGE_FILE = './static_image.png'  # Replace with your image file path (static image for video)

# Get list of audio files
AUDIO_FILES = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav', '.flac'))]

# Ensure the music directory exists
if not AUDIO_FILES:
    print("No music files found in the specified directory.")
    exit()

# Replace with your YouTube stream URL
stream_key = "m5dp-tt7s-e18e-gze0-3gge"  # Replace with your actual stream key
rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

# Function to stream to YouTube using streamlink
def stream_audio():
    while True:
        # Randomly select an audio file from the list
        audio_file = random.choice(AUDIO_FILES)
        audio_path = os.path.join(MUSIC_DIR, audio_file)

        print(f"Streaming audio: {audio_file}")

        # Use streamlink with a static image (using FFmpeg as a backend)
        ffmpeg_command = [
            'streamlink', 
            'rtmp://a.rtmp.youtube.com/live2', 
            'audio',  # Placeholder for audio stream, streamlink would auto-connect.
            '--hls-duration', '5',  # Adjust HLS duration
            '--hls-segment-threads', '2', 
            '--player-passthrough', 'ffmpeg',  # Use FFmpeg internally
            '--ffmpeg-opts', f'-re -i {audio_path} -loop 1 -i {IMAGE_FILE} -c:v libx264 -preset veryfast -c:a aac -b:a 128k -f flv {rtmp_url}'
        ]

        # Start streaming process
        try:
            streamlink_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = streamlink_process.communicate()

            if streamlink_process.returncode != 0:
                print(f"Error: {stderr.decode()}")
            else:
                print(f"Streaming started successfully: {audio_file}")

        except Exception as e:
            print(f"Error while streaming audio file {audio_file}: {e}")

        time.sleep(5)  # Pause for 5 seconds before switching to the next track

# Start the stream
if __name__ == "__main__":
    stream_audio()

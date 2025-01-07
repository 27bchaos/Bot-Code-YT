import os
import time
from flask import Flask, Response
import ffmpeg

app = Flask(__name__)

# Directory containing your music files (replace with the actual path)
MUSIC_DIR = '/path/to/your/music/files'
AUDIO_FILES = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav', '.flac'))]

# Function to stream the audio files
def stream_audio():
    while True:
        for file in AUDIO_FILES:
            file_path = os.path.join(MUSIC_DIR, file)
            # Using FFmpeg to convert audio file to a format suitable for streaming
            process = (
                ffmpeg
                .input(file_path)
                .output('pipe:1', format='mp3', acodec='libmp3lame', ar='44100', ac=2)
                .run_async(pipe_stdout=True, pipe_stderr=True)
            )
            while True:
                # Yield the audio data to Flask for continuous streaming
                data = process.stdout.read(1024)
                if not data:
                    break
                yield data
            process.stdout.close()
            process.wait()

        # Optional: Sleep before starting the next loop (adjust depending on how often you want to repeat the music)
        time.sleep(5)

# Route for the audio stream
@app.route('/stream')
def stream():
    return Response(stream_audio(), content_type='audio/mpeg')

# Start the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)

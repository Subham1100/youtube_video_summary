from pytube import YouTube
import whisper
from transformers import pipeline
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = "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"

# Load the Whisper model during application startup and store it in the app context
model = whisper.load_model("base")


def download_and_summarize_youtube_video(youtube_video_url):
    # Create a YouTube object
    yt = YouTube(youtube_video_url)

    # Get the video title and thumbnail URL
    video_title = yt.title
    video_title_cleaned = video_title.replace(" ", "") + ".mp3"
    thumbnail_url = yt.thumbnail_url

    # Get the audio stream
    audio_stream = yt.streams.filter(only_audio=True).first()

    if audio_stream is not None:
        # Download the audio to the specified output path (folder "audio" in this case)
        output_path = "audio"
        audio_stream.download(output_path=output_path, filename=video_title_cleaned)
        print("Audio downloaded successfully!")
        # Access the downloaded audio file and read its content into a variable
        audio_file_path = f"{output_path}/{video_title_cleaned}"
        with open(audio_file_path, "rb") as file:
            audio_data = file.read()

        # Access the loaded Whisper model from the app context
        result = model.transcribe(audio_file_path)
        transcript = result["text"]
        # print(transcript)

        return video_title, transcript, thumbnail_url

    else:
        print("No audio stream found for download.")
        return None, None, None


@app.route('/summarize', methods=['POST'])
def summarize_video():
    try:
        youtube_video_url = request.json.get('youtube_video_url')
        video_title, transcript, thumbnail_url = download_and_summarize_youtube_video(youtube_video_url)
        response = {
            'video_title': video_title,
            'transcript': transcript,
            'thumbnail_url': thumbnail_url
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='127.0.0.1', port=5003)

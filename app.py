from flask import Flask, render_template, request, jsonify
import time
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

# Function to get YouTube transcript
def get_youtube_transcript(video_url):
    video_id = video_url.split("=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    result = " ".join([x['text'] for x in transcript])
    return result

# Initialize BERT-based summarization pipeline
summarizer = pipeline("summarization")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    if request.method == 'POST':
        try:
            video_url = request.json['video_url']  # Accessing form data sent as JSON
            # Get YouTube transcript
            transcript_text = get_youtube_transcript(video_url)

            # Perform summarization in chunks of 1000 characters
            summarized_text = []
            total_chunks = (len(transcript_text) // 1000) + 1  # Calculate total number of chunks
            print("Processing... [", end="", flush=True)
            for i in range(0, len(transcript_text), 1000):
                chunk = transcript_text[i:i+1000]
                summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
                summarized_text.append(summary[0]['summary_text'])

                # Print loading progress
                progress = (i + 1000) / len(transcript_text) * 100
                print("#", end="", flush=True)
                time.sleep(0.1)  # Simulate processing time

            print("] 100%")

            original_text = transcript_text
            summarized_text = " ".join(summarized_text)

            response = {
                "original_text": original_text,
                "summarized_text": summarized_text
            }
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

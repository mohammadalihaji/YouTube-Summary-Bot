import os
from flask import Flask, request, jsonify, render_template_string
from google import genai
from google.genai.errors import APIError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend JS to call backend

# --- Initialize Gemini Client ---
try:
    client = genai.Client()
    print("Gemini Client initialized successfully.")
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("FATAL: Ensure GEMINI_API_KEY environment variable is set correctly.")

# --- Function to summarize YouTube video ---
def summarize_youtube_video(youtube_url: str):
    """
    Summarizes a YouTube video into 5 bullet points using Gemini API.
    """
    prompt = (
        "You are an expert video summarization bot. "
        "Analyze the content of this YouTube video and provide a "
        "**concise summary of the main points**. "
        "The output **must be a list of exactly 5 bullet points**, "
        "with each point being a full sentence, using the markdown '*' character for the list."
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                # YouTube video as file URI
                genai.types.Part.from_uri(file_uri=youtube_url, mime_type="video/mp4"),
                prompt
            ],
        )
        return response.text, 200

    except APIError as e:
        error_msg = f"API Error: {e}"
        print(error_msg)
        return error_msg, 500
    except Exception as e:
        error_msg = f"Unexpected Error: {e}"
        print(error_msg)
        return error_msg, 500

# --- Route to serve HTML frontend ---
@app.route("/", methods=["GET"])
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return render_template_string(html_content)

# --- Route for summarization API ---
@app.route("/summarize", methods=["POST"])
def handle_summarize():
    try:
        data = request.get_json()
        youtube_url = data.get("youtube_link")
        if not youtube_url:
            return jsonify({"error": "Missing 'youtube_link' in request."}), 400

        summary_text, status_code = summarize_youtube_video(youtube_url)

        if status_code == 200:
            return jsonify({"summary": summary_text}), 200
        else:
            return jsonify({"error": summary_text}), status_code

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

# --- Main execution ---
if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True, port=5000, use_reloader=False)

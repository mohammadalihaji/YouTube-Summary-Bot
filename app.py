import os
from flask import Flask, request, jsonify, render_template_string
from google import genai
from google.genai.errors import APIError
from flask_cors import CORS
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)
CORS(app)

# --- Helper: Normalize YouTube URLs ---
def normalize_youtube_url(url: str) -> str:
    """
    Converts different YouTube URL formats (mobile, short, etc.)
    into a standard desktop YouTube link.
    """
    try:
        parsed = urlparse(url)

        # youtu.be short link
        if "youtu.be" in parsed.netloc:
            video_id = parsed.path.lstrip("/")
            return f"https://www.youtube.com/watch?v={video_id}"

        # m.youtube.com link
        if "m.youtube.com" in parsed.netloc:
            video_id = parse_qs(parsed.query).get("v", [None])[0]
            if video_id:
                return f"https://www.youtube.com/watch?v={video_id}"

        # youtube.com with /watch?v=
        if "youtube.com" in parsed.netloc and "v=" in parsed.query:
            return url

        return url
    except Exception:
        return url

# --- Initialize Gemini Client ---
try:
    client = genai.Client()
    print("Gemini Client initialized successfully.")
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("FATAL: Ensure GEMINI_API_KEY environment variable is set correctly.")

# --- Summarization Function ---
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
                genai.types.Part.from_uri(file_uri=youtube_url, mime_type="video/mp4"),
                prompt
            ],
        )
        return response.text, 200
    except APIError as e:
        return f"API Error: {e}", 500
    except Exception as e:
        return f"Unexpected Error: {e}", 500

# --- Serve HTML frontend ---
@app.route("/", methods=["GET"])
def index():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return render_template_string(html_content)
    except FileNotFoundError:
        return "<h3>index.html not found. Please add it to your project root.</h3>", 404

# --- API Route ---
@app.route("/summarize", methods=["POST"])
def handle_summarize():
    try:
        data = request.get_json()
        youtube_url = data.get("youtube_link")

        if not youtube_url:
            return jsonify({"error": "Missing 'youtube_link' in request."}), 400

        # Normalize before processing
        youtube_url = normalize_youtube_url(youtube_url)

        summary_text, status_code = summarize_youtube_video(youtube_url)

        if status_code == 200:
            return jsonify({"summary": summary_text}), 200
        else:
            return jsonify({"error": summary_text}), status_code

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

# --- Main ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

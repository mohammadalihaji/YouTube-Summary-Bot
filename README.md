# YouTube-Summary-Bot
YouTube Summary Bot made by Haji MohammadAli
🎥 Gemini YouTube Video Summarizer
This is a full-stack, local web application that uses the Gemini API via a Python Flask backend to generate a concise 5-point summary for any public YouTube video link.

✨ Features
Multimodal Input: Directly processes a YouTube URL using the gemini-2.5-flash model.

Structured Output: Generates a structured summary consisting of exactly five bullet points.

Local Backend: Uses Flask to securely handle the Gemini API key and process requests.

Modern Frontend: A clean, responsive user interface built with HTML, Tailwind CSS, and JavaScript.

🛠️ Prerequisites
Before starting, ensure you have the following installed and configured:

Python: Python 3.8+ installed on your system.

Gemini API Key: Obtain a free API key from Google AI Studio.

🚀 Setup and Installation
Step 1: Clone the Repository (Local Setup)
Save the following three files in the same directory:

app.py (The Flask Backend)

index.html (The Web Frontend)

requirements.txt (This file)

Step 2: Install Python Dependencies
Open your terminal in the project directory and run the following command to install Flask, the Gemini SDK, and CORS support:

pip install -r requirements.txt

Step 3: Configure API Key
The application secures your API key by reading it from an environment variable named GEMINI_API_KEY.

Set your API Key in the terminal session:

Operating System

Command

Linux/macOS

export GEMINI_API_KEY="YOUR_API_KEY_HERE"

Windows (CMD)

set GEMINI_API_KEY="YOUR_API_KEY_HERE"

Windows (PowerShell)

$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"

Replace "YOUR_API_KEY_HERE" with the actual key you obtained.

▶️ How to Run the Application
The application requires two components to run simultaneously: the Python server and the HTML frontend.

1. Start the Flask Backend
In your terminal (where the GEMINI_API_KEY is set), run the app.py file:

python app.py

The terminal will confirm that the server is running:

* Running on [http://127.0.0.1:5000](http://127.0.0.1:5000)

Keep this terminal window open and running.

2. Open the Frontend
You have two ways to access the application in your browser:

Option A (Recommended - Opens HTML Directly): Find the index.html file on your computer and double-click it. It will open in your browser using a file:// URL. The JavaScript inside will communicate with your running Flask server.

Option B (Access via Flask Route): Open your browser and navigate to: http://127.0.0.1:5000/. The app.py file is configured to serve the index.html file at this base route.

3. Use the Summarizer
Paste a public YouTube video URL into the input box.

Click the Summarize Video button.

The request will be sent to the Flask server, which calls the Gemini API, and the 5-point summary will appear on the screen.

from flask import Flask, request, jsonify
import openai
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI()

# Recommendation function
def get_manga_recommendation(preferred_genre, last_read_manga, complete_series):
    prompt = f"""
    Based on the preferred genre '{preferred_genre}', last-read manga '{last_read_manga}', 
    and preference for a complete series ('{complete_series}'), recommend a similar manga title.
    """
    response = llm(prompt)
    return response.strip()

# Route for recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    preferred_genre = data.get('preferred_genre', '')
    last_read_manga = data.get('last_read_manga', '')
    complete_series = data.get('complete_series', '')
    recommendation = get_manga_recommendation(preferred_genre, last_read_manga, complete_series)
    return jsonify({'recommendation': recommendation})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

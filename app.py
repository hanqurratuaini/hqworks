from flask import Flask, request, jsonify, render_template
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

# Function to create MoM based on user input
def create_mom(title, date, attendees, notes):
    # Format attendees
    formatted_attendees = ""
    for group in attendees:
        group_name = group.get("group_name", "")
        members = group.get("members", "")
        formatted_attendees += f"\n{group_name}:\n"
        formatted_attendees += "\n".join([f"- {member}" for member in members.split("|")])

    # Create the prompt
    prompt = f"""
    Create a Minutes of Meeting (MoM) based on the following details:
    Title: {title}
    Date: {date}
    Attendees: {formatted_attendees}
    Notes: {notes}
    Format the MoM with clear sections for 'Action Items' and 'Meeting Notes'.
    """
    # Use LangChain's OpenAI instance to generate response
    response = llm(prompt)
    
    return response.strip()

# Route to render the front-end page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle MoM generation
@app.route('/generate_mom', methods=['POST'])
def generate_mom():
    data = request.get_json()
    title = data.get('title', '')
    date = data.get('date', '')
    attendees = data.get('attendees', [])
    notes = data.get('notes', '')
    
    # Generate the MoM
    mom = create_mom(title, date, attendees, notes)
    return jsonify({'mom': mom})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
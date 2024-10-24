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

# Function to create MoM based on user input and handle long notes
def create_mom(title, date, attendees, notes):
    # Format attendees based on the desired output
    formatted_attendees = ""
    for group in attendees:
        group_name = group.get("group_name", "")
        members = group.get("members", "")
        member_list = [f"{idx + 1}. {member.strip()}" for idx, member in enumerate(members.split(";"))]
        formatted_attendees += f"{group_name}:\n" + "\n".join(member_list) + "\n\n"

    # Create a single prompt with the entire input
    prompt = f"""
    Create a Minutes of Meeting (MoM) based strictly on the details provided below.
    Do not add any extra information that is not present in the input:
    Title: {title}
    Date: {date}
    Attendees: {formatted_attendees}
    Notes: {notes}
    Structure:
    1. Title
    2. Date
    3. Attendee List
    4. Action Items (concise)
    5. Discussion Points (detailed, only use information provided in the Notes)
    """

    try:
        response = llm(prompt)
        output = response.strip()
        return output
    except openai.error.InvalidRequestError as e:
        # Handle token limit errors
        return "Error: The input is too long to process. Please shorten the notes or attendees."

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

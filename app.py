from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))def ask_ai(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an intelligent learning assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return response.choices[0].message.content

@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.json["text"]
    result = ask_ai(f"Summarize these notes clearly:\n{text}")
    return jsonify({"summary": result})

@app.route("/flashcards", methods=["POST"])
def flashcards():
    text = request.json["text"]
    result = ask_ai(
        f"Create short flashcards from these notes. Format as bullet points:\n{text}"
    )
    cards = result.split("\n")
    return jsonify({"cards": cards})

@app.route("/quiz", methods=["POST"])
def quiz():
    text = request.json["text"]
    result = ask_ai(f"Create 5 quiz questions from these notes:\n{text}")
    questions = result.split("\n")
    return jsonify({"questions": questions})

if __name__ == "__main__":
    app.run(debug=True)
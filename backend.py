from flask import Flask, request, jsonify, render_template
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Create OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ API Key is missing! Check your .env file.")
else:
    print("✅ API Key Loaded Successfully!")

client = OpenAI()  # Correct way to initialize OpenAI client

@app.route("/")
def home():
    return render_template("frontend.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    print("📩 Message from frontend:", user_message)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful chatbot."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        print("🤖 Bot reply:", reply)
        return jsonify({"response": reply})

    except Exception as e:
        print("❌ Error from OpenAI:", repr(e))
        return jsonify({"response": "Oops! Something went wrong."})

if __name__ == "__main__":
    app.run(debug=True)

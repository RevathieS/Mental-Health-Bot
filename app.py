from flask import Flask, request, jsonify, render_template
import ollama
from flask_cors import CORS
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')  # Required for Sentiment Analysis

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

sia = SentimentIntensityAnalyzer()

@app.route("/")
def home():
    return render_template("index.html")  # Serve chatbot UI

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    sentiment_score = sia.polarity_scores(user_message)
    sentiment = "neutral"
    if sentiment_score["compound"] >= 0.05:
        sentiment = "positive"
    elif sentiment_score["compound"] <= -0.05:
        sentiment = "negative"

    if "first_message" in data and data["first_message"]:
        bot_reply = "I'm here for you. What's wrong? How can I help?"
    else:
        prompt = f"""
        The user wants to talk. Keep responses short and supportive.
        - Keep it conversational and natural.
        - Avoid overwhelming information; let the user share more.

        **User's message:** {user_message}
        **Your Response:**
        """
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        bot_reply = response["message"]["content"]

    return jsonify({"response": bot_reply, "sentiment": sentiment})

if __name__ == "__main__":
    app.run(debug=True)

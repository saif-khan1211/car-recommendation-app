from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

from car_recommender.config import load_config
from car_recommender.model import load_model, predict
from car_recommender.preprocessing import preprocess_input
from car_recommender.explain import explain_prediction
from flask import send_from_directory
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY") 
config = load_config()


model_path = config['model']['path']
model = load_model(model_path) 


app = Flask(__name__)
CORS(app)

@app.route("/predict", methods=["POST"])
def predict_route():
    data = request.get_json()
    df = preprocess_input(data)
    tier, score = predict(model, df)
    return jsonify({"value_tier": tier, "probability_score": score})






@app.route("/explain", methods=["POST"])
def explain_route():
    data = request.get_json()
    df = preprocess_input(data)
    tier, score = predict(model, df)
    explanation = explain_prediction(data, tier, score)
    return jsonify({
        "value_tier": tier,
        "probability_score": score,
        "explanation": explanation
    })


@app.route("/")
def serve_index():
    # Serve static/index.html at the root
    return send_from_directory("static", "index.html")

@app.route("/<path:path>")
def serve_static(path):
    # Serve any other files in static/, like JS and CSS
    return send_from_directory("static", path)






if __name__ == "__main__":
    app.run(
        host=config["api"]["host"],
        port=config["api"]["port"]
    )



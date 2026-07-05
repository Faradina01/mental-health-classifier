from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import predict_sentence

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API Klasifikasi Kesehatan Mental Aktif"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not data or "text" not in data:
        return jsonify({"error": "Field 'text' wajib diisi"}), 400

    text = data["text"]
    if not text.strip():
        return jsonify({"error": "Teks tidak boleh kosong"}), 400

    result = predict_sentence(text)
    return jsonify(result)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
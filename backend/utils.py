import re
import os
import requests
import pickle
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Input, Embedding, SpatialDropout1D, LSTM,
    GlobalMaxPooling1D, Dense, Dropout
)
from tensorflow.keras.preprocessing.sequence import pad_sequences

MAX_LEN = 300
VOCAB_SIZE = 31777
EMBEDDING_DIM = 300

model = Sequential([
    Input(shape=(MAX_LEN,)),
    Embedding(VOCAB_SIZE, EMBEDDING_DIM),
    SpatialDropout1D(0.3),
    LSTM(128, return_sequences=True, dropout=0.3),
    GlobalMaxPooling1D(),
    Dense(128, activation="relu"),
    Dropout(0.6),
    Dense(4, activation="softmax")
])

# PENTING: pakai file .h5 yang ASLI (bukan yang di-convert ke .keras)
MODEL_PATH = "model/best_fasttext_lstm.h5"

if not os.path.exists(MODEL_PATH):
    print("Downloading model...")

    url = "https://github.com/Faradina01/mental-health-classifier/releases/download/v1.0/best_fasttext_lstm.h5"

    r = requests.get(url, allow_redirects=True)
    r.raise_for_status()

    os.makedirs("model", exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        f.write(r.content)

print("Loading model...")
model.load_weights(MODEL_PATH)

with open("model/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("model/label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"www\S+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-zA-Z\s']", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def predict_sentence(text):
    cleaned = clean_text(text)
    seq = tokenizer.texts_to_sequences([cleaned])
    pad = pad_sequences(seq, maxlen=MAX_LEN, padding="post", truncating="post")
    pred = model.predict(pad, verbose=0)
    idx = int(np.argmax(pred))
    confidence = float(np.max(pred))
    label = le.classes_[idx]
    return {"label": label, "confidence": confidence}
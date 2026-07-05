from utils import model, tokenizer, le, clean_text
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

MAX_LEN = 300

test_sentences = [
    "I feel hopeless and want to die",
    "I had a great time with my friends at the park today",
    "My hands were shaking before the exam started",
    "I don't have the energy to get out of bed most mornings",
    "asdkj qweiu zxcvb random gibberish text nonsense"
]

for text in test_sentences:
    cleaned = clean_text(text)
    seq = tokenizer.texts_to_sequences([cleaned])
    print(f"\nText: {text}")
    print(f"Cleaned: {cleaned}")
    print(f"Token sequence: {seq}")

    pad = pad_sequences(seq, maxlen=MAX_LEN, padding="post", truncating="post")
    pred = model.predict(pad, verbose=0)[0]

    for label, prob in zip(le.classes_, pred):
        print(f"  {label}: {prob:.4f}")
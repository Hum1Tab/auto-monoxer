from flask import Flask, render_template, jsonify
import pytesseract
import time
import threading
from PIL import ImageGrab
import re
import unicodedata
import os
import string
from fuzzywuzzy import fuzz

# Tesseractのパスを明示（インストール先に合わせて変更）
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
current_answer = ""

def normalize(text):
    return unicodedata.normalize("NFKC", text.strip())

def load_data():
    data_path = os.path.join(os.path.dirname(__file__), "data.txt")
    with open(data_path, encoding='utf-8') as f:
        return {normalize(line.split(":", 1)[0]): line.split(":", 1)[1] for line in f if ':' in line}

def remove_spaces(text):
    return text.replace(" ", "").replace("　", "")

def remove_symbols(text):
    # 記号・句読点・カンマ・カッコ・全角記号も除去
    text = re.sub(r'[\s\u3000]', '', text)  # スペース全除去
    text = re.sub(r'[\u3001\u3002\uff08\uff09\(\)\.,、。・「」『』【】［］〈〉《》“”‘’\-\—\–\[\]{}:：;；!！?？"\'\\/]', '', text)
    return text

def screen_monitor():
    global current_answer
    word_map = load_data()
    last_a = None

    while True:
        img = ImageGrab.grab()  # スクリーン全体
        text = pytesseract.image_to_string(img, lang="jpn")  # 日本語OCR
        text = normalize(text)
        text_clean = remove_symbols(text)
        print("OCR結果:", text)
        best_score = 0
        best_answer = None
        for a, b in word_map.items():
            a_clean = remove_symbols(a)
            score = fuzz.partial_ratio(a_clean, text_clean)
            if score > best_score and score >= 80:
                best_score = score
                best_answer = b
        if best_answer and current_answer != best_answer:
            current_answer = best_answer
        time.sleep(0.2)  # 負荷軽減のため0.2秒待つ（高速化）

@app.route("/")
def index():
    return render_template("index.html", answer=current_answer)

@app.route("/api/answer")
def api_answer():
    return jsonify({"answer": current_answer})

def run_monitor():
    thread = threading.Thread(target=screen_monitor)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    run_monitor()
    app.run(debug=True)

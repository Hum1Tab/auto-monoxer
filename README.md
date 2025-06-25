# monoxer OCR 答え表示アプリ

## 概要

このアプリは、画面上の問題文をOCRで自動認識し、`data.txt`に登録された問題文と照合して、答えをWeb画面中央に大きく表示します。答えは自動でリアルタイムに切り替わります。

## 必要環境

- Python 3.x
- Flask
- pytesseract
- Pillow
- fuzzywuzzy
- Tesseract OCR（Windows用: `C:\Program Files\Tesseract-OCR\tesseract.exe` にインストール）
- data.txt（問題文:答え の形式で保存）

## インストール

```bash
pip install flask pytesseract pillow fuzzywuzzy python-Levenshtein
```

Tesseract OCRを[公式サイト](https://github.com/tesseract-ocr/tesseract)からインストールしてください。

## 使い方

1. `data.txt` に「問題文: 答え」の形式で問題と答えを登録します。
2. `app.py` を実行します。

```bash
python app.py
```

3. ブラウザで `http://localhost:5000/` にアクセスすると、答えが画面中央に大きく表示されます。

## ファイル構成

- `app.py` : メインアプリケーション
- `data.txt` : 問題文と答えのデータ
- `templates/index.html` : 答え表示用Webページ
- `README.md` : このファイル

## 備考

- OCRは画面全体を0.2秒ごとに自動取得します。
- 答えは1秒ごとにWeb画面で自動更新されます。
- Tesseractのパスは環境に合わせて変更してください。

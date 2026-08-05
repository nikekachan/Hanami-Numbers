from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

# サーバー上のデータファイルを読み込む
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"daily": {}, "targets": {}, "forum": []}

# サーバー上にデータファイルを書き込む
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

# 全端末共有用データ取得API
@app.route('/api/get_all_data', methods=['GET'])
def get_all_data():
    return jsonify(load_data())

# 全端末共有用データ一括保存API
@app.route('/api/save_all_data', methods=['POST'])
def save_all_data():
    try:
        data = request.json
        save_data(data)
        return jsonify({"status": "success", "message": "☁️ サーバーへ正常に保存されました！"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
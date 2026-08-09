from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# JSONBin（永久保存用データベース）情報
BIN_ID = '6a77edbeda38895dfecbdb48'
API_KEY = '$2a$10$92xqDnm1PpFIMdMZAQN4ruvsIahgOinrURJkZVdAW.ErjgBSWysYG'

JSONBIN_URL = f'https://api.jsonbin.io/v3/b/{BIN_ID}'
HEADERS = {
    'Content-Type': 'application/json',
    'X-Master-Key': API_KEY
}

def load_data():
    try:
        res = requests.get(f'{JSONBIN_URL}/latest', headers=HEADERS)
        if res.status_code == 200:
            return res.json().get('record', {"daily": {}, "targets": {}, "forum": []})
    except Exception as e:
        print("Load Error:", e)
    return {"daily": {}, "targets": {}, "forum": []}

def save_data(data):
    try:
        requests.put(JSONBIN_URL, headers=HEADERS, json=data)
    except Exception as e:
        print("Save Error:", e)

# 通常入力・管理者用ページ
@app.route('/')
def index():
    return render_template('index.html')

# 📱 一般スタッフ閲覧専用URL
@app.route('/view')
def view_only():
    return render_template('index.html')

@app.route('/api/get_all_data', methods=['GET'])
def get_all_data():
    return jsonify(load_data())

@app.route('/api/save_all_data', methods=['POST'])
def save_all_data():
    try:
        data = request.json
        save_data(data)
        return jsonify({"status": "success", "message": "☁️ 保管庫へ正常保存されました！"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

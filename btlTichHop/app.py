from flask import Flask, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["tiktok_db"]
collection = db["tiktok_data"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/videos', methods=['GET'])
def get_videos():
    videos = list(collection.find({}, {"_id": 0}))  # Lấy dữ liệu bỏ _id
    return jsonify(videos)

if __name__ == '__main__':
    app.run(debug=True)

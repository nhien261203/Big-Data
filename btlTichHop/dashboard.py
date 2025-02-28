import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from pymongo import MongoClient

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["tiktok_db"]
collection = db["tiktok_data"]

# Lấy dữ liệu từ MongoDB
data = list(collection.find({}, {"_id": 0}))  # Loại bỏ ObjectId
df = pd.DataFrame(data)

# Đọc dữ liệu từ CSV (bổ sung)
csv_file = "tiktok_dataset.csv"
df_csv = pd.read_csv(csv_file)

df = pd.concat([df, df_csv], ignore_index=True)  # Gộp dữ liệu

# Kiểm tra dữ liệu
if df.empty:
    print("⚠️ Cảnh báo: Không có dữ liệu!")
    df = pd.DataFrame(columns=["video_like_count", "video_view_count", "video_share_count", "video_download_count", "video_comment_count"])  
else:
    print(f"✅ Đã tải {len(df)} bản ghi từ MongoDB và CSV.")
    print(f"📌 Các cột: {df.columns.tolist()}")

# Biểu đồ
fig_likes = px.histogram(df, x="video_like_count", title="📊 Biểu đồ số lượt thích")
fig_views = px.histogram(df, x="video_view_count", title="📊 Biểu đồ số lượt xem")
fig_shares = px.histogram(df, x="video_share_count", title="📊 Biểu đồ số lượt chia sẻ")
fig_downloads = px.histogram(df, x="video_download_count", title="📊 Biểu đồ số lượt tải xuống")
fig_comments = px.histogram(df, x="video_comment_count", title="📊 Biểu đồ số lượt bình luận")

# Khởi tạo ứng dụng Dash
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("📊 TikTok Data Dashboard"),
    dcc.Graph(figure=fig_likes),
    dcc.Graph(figure=fig_views),
    dcc.Graph(figure=fig_shares),
    dcc.Graph(figure=fig_downloads),
    dcc.Graph(figure=fig_comments),
])

# Chạy server
if __name__ == '__main__':
    app.run_server(debug=True, port=8060)
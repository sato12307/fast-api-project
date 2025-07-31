from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from supabase import create_client

# Supabaseの認証情報を環境変数から取得
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Supabaseクライアント初期化
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# FastAPIアプリ初期化
app = FastAPI()

# CORS設定（Gradioやブラウザからアクセスできるようにする）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて制限してもOK
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データモデル
class Data(BaseModel):
    text: str

# POSTエンドポイント
@app.post("/save")
async def save_data(data: Optional[Data]):
    if data is None:
        return {"error": "データが送信されていません。"}

    print("RECEIVED:", data.text)

    # Supabaseに保存する例
    try:
        result = supabase.table("your_table_name").insert({"text": data.text}).execute()
        return {"status": "success", "result": result.data}
    except Exception as e:
        print("Supabase保存エラー:", e)
        return {"error": str(e)}

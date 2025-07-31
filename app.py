from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client
import uuid
import os

# Supabase 認証情報（環境変数から取得）
#こんにちは
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Supabaseクライアント初期化
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# FastAPI 初期化
app = FastAPI()

# CORS設定（Gradio/ブラウザからのリクエスト許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では限定すべき
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 受け取るデータの形式
class TextData(BaseModel):
    content: str

# 保存処理エンドポイント
@app.post("/save")
async def save_text(data: TextData):
    try:
        # 一意のファイル名を生成
        filename = f"{uuid.uuid4()}.txt"
        text = data.content


         #✅ str → bytes に変換（Supabaseが期待する形式）
        text_bytes = BytesIO(text.encode("utf-8"))

        # Supabaseにアップロード
        res = supabase.storage.from_("mental-library").upload(
            filename, text, {"content-type": "text/plain"}
        )

        # アップロード結果の確認とURL構築
        if res.get("data") and res["data"].get("path"):
            path = res["data"]["path"]
            public_url = f"{SUPABASE_URL}/storage/v1/object/public/mental-library/{path}"
            return {"success": True, "public_url": public_url}
        else:
            return {"success": False, "error": res.get("error") or "No path returned"}

    except Exception as e:
        return {"success": False, "error": str(e)}

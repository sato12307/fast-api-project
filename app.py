import os
from fastapi import FastAPI, Request
from supabase import create_client, Client
from io import BytesIO
from uuid import uuid4

app = FastAPI()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.post("/save")
async def save_text(request: Request):
    data = await request.json()
    text = data.get("text")
    filename = data.get("filename", f"mental_{uuid4().hex}.txt")

    # 保存用オブジェクト
    file_obj = BytesIO(text.encode("utf-8"))

    # Supabaseにアップロード
    result = supabase.storage.from_("mental-library").upload(filename, file_obj)

    # ✅ 公開URLを自前で構築
    public_url = f"{SUPABASE_URL}/storage/v1/object/public/mental-library/{filename}"

    return {
        "status": "success",
        "uploaded": filename,
        "public_url": public_url
    }

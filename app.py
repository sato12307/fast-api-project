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
    text = data["text"]
    filename = data.get("filename", f"mental_{uuid4().hex}.txt")

    file_obj = BytesIO(text.encode("utf-8"))

    result = supabase.storage.from_("mental-library").upload(filename, file_obj)

    return {"status": "success", "uploaded": filename, "supabase_result": result}

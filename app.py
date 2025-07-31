from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
BUCKET_NAME = "mental-library"

@app.post("/save")
async def save_text(request: Request):
    data = await request.json()
    content = data.get("text")
    filename = data.get("filename", "entry.txt")

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "text/plain"
    }

    upload_url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{filename}"

    async with httpx.AsyncClient() as client:
        response = await client.post(upload_url, headers=headers, content=content)

    return {"status": response.status_code, "detail": response.text}

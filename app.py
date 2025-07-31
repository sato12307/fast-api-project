from fastapi import FastAPI, Form
import httpx
import base64

app = FastAPI()

SUPABASE_URL = "https://hxpvsaeablssivlgrlbc.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh4cHZzYWVhYmxzc2l2bGdybGJjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM5NjUyMDcsImV4cCI6MjA2OTU0MTIwN30.kROV7wqNjyKO5JofFcazoaYzLzOUU-oNLOyHOf60-1w"
BUCKET_NAME = "mental-library"

@app.post("/save")
async def save_diary(filename: str = Form(...), content: str = Form(...)):
    file_path = f"{filename}.txt"
    file_bytes = content.encode("utf-8")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{file_path}",
            headers={
                "apikey": SUPABASE_API_KEY,
                "Authorization": f"Bearer {SUPABASE_API_KEY}",
                "Content-Type": "text/plain"
            },
            content=file_bytes
        )

    if response.status_code == 200:
        return {"message": "保存完了", "filename": file_path}
    else:
        return {"error": response.status_code, "detail": response.text}

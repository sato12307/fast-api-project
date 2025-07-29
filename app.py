from datetime import datetime
from fastapi import FastAPI, Request
import os

# 保存先フォルダ
SAVE_DIR = "logs"
os.makedirs(SAVE_DIR, exist_ok=True)

app = FastAPI()

@app.post("/")
async def save_text(request: Request):
    data = await request.json()
    text = data.get("text", "")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(SAVE_DIR, f"entry_{timestamp}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    return {"message": "保存しました", "filename": filename}

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/save")
async def save_data(request: Request):
    data = await request.json()
    text = data.get("text", "")
    print(f"Received text: {text}")
    return JSONResponse(content={"status": "success", "received": text})

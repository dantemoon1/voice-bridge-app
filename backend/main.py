import os
from fastapi import FastAPI, WebSocket
import asyncio
import httpx
from livekit import rtc

app = FastAPI()

# Poke Voice Bridge Ingest URL
POKE_INGEST_URL = "https://poke.com/api/v1/ingest/5c57af82-b6b4-4b16-a9dd-94a30a22cf81"

@app.get("/")
async def root():
    return {"message": "Voice Bridge API is running"}

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async with httpx.AsyncClient() as client:
        try:
            while True:
                data = await websocket.receive_bytes()
                # Forward audio chunks to Poke Ingest
                await client.post(POKE_INGEST_URL, content=data)
        except Exception as e:
            print(f"Streaming error: {e}")
        finally:
            await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

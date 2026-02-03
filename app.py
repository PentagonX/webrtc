from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

clients = {
    "viewer": None,
    "streamer": None
}

@app.get("/")
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws/{role}")
async def websocket_endpoint(ws: WebSocket, role: str):
    await ws.accept()
    clients[role] = ws
    print(f"{role} connected")

    try:
        while True:
            msg = await ws.receive_text()

            target = "viewer" if role == "streamer" else "streamer"
            if clients.get(target):
                await clients[target].send_text(msg)

    except WebSocketDisconnect:
        print(f"{role} disconnected")
        clients[role] = None

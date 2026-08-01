from fastapi import FastAPI, WebSocket, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Command(BaseModel):
    action: str


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "HTTP Pilot"
        },
    )


@app.post("/command")
async def command(cmd: Command):
    print(f"Command Recived: {cmd.action}")

    return {
        "status": "ok"
    }


@app.websocket("/ws")
async def websocket(ws: WebSocket):
    await ws.accept()

    try:
        while True:
            message = await ws.receive_text()

            print(f"WS: {message}")

            await ws.send_text(f"Captured: {message}")

    except Exception:
        print("Client disconnected")
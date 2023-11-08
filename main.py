from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from entities import Email
from websocket import ConnectionManager

app = FastAPI()

manager = ConnectionManager()

templates = Jinja2Templates(directory="templates")


@app.get("/group/{group}/client/{client}", response_class=HTMLResponse)
async def get(request: Request, group: str, client: str):
    return templates.TemplateResponse("chat.html.j2", {
        "request": request,
        "group": group,
        "client": client})


@app.websocket("/ws/group/{group}/client/{client}")
async def websocket_endpoint(websocket: WebSocket, group: str, client: str):
    await manager.connect(websocket, group)
    try:
        while True:
            data = await websocket.receive_json()
            email = Email(sender=data["sender"], group=data["group"], message=data["message"])
            await manager.send_group(email.model_dump(), group)
    except WebSocketDisconnect:
        manager.disconnect(websocket, group)

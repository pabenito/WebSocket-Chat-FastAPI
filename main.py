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
    return templates.TemplateResponse("index.html.j2", {
        "request": request,
        "group_id": group,
        "client_id": client})


@app.websocket("/ws/group/{id}/client/{client}")
async def websocket_endpoint(websocket: WebSocket, id: str, client: str):
    await manager.connect(websocket, id)
    try:
        while True:
            data = await websocket.receive_json()
            email = Email(sender=data["sender"], to=data["to"], message=data["message"])
            await manager.send_single(email.model_dump(), websocket)
            await manager.send_group(email.model_dump(), id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, id)

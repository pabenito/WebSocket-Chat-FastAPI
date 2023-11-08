from typing import Dict
from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, group: str):
        await websocket.accept()
        if not group in self.active_connections:
            self.active_connections[group] = []
        self.active_connections[group].append(websocket)

    def disconnect(self, websocket: WebSocket, group: str):
        self.active_connections[group].remove(websocket)

    async def send_group(self, message, group: str):
        for connection in self.active_connections[group]:
            await connection.send_json(message)
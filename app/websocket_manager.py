from fastapi import WebSocket
from typing import Dict, List


class ConnectionManager:
    def __init__(self):
        # room_name: List[WebSocket]
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_name: str):
        await websocket.accept()
        if room_name not in self.active_connections:
            self.active_connections[room_name] = []
        self.active_connections[room_name].append(websocket)

    async def disconnect(self, websocket: WebSocket, room_name: str):
        self.active_connections[room_name].remove(websocket)
        if not self.active_connections[room_name]:
            del self.active_connections[room_name]

    async def broadcast(self, message: dict, room_name: str):
        if room_name in self.active_connections:
            for connection in self.active_connections[room_name]:
                await connection.send_json(message)


manager = ConnectionManager()

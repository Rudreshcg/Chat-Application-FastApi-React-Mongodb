from fastapi import WebSocket
from controllers import set_room_activity
import logging
from typing import List
from starlette.websockets import WebSocketState, WebSocketDisconnect

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, room_name: str):
        await websocket.accept()
        await set_room_activity(room_name, True)
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket, room_name: str):
        self.active_connections.remove(websocket)
        if len(self.active_connections) == 0:
            await set_room_activity(room_name, False)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    # async def broadcast(self, message: str):
    #     logger.debug(f"Broadcasting across {len(self.active_connections)} CONNECTIONS")
    #     for connection in self.active_connections:
    #         if connection.application_state == WebSocketState.CONNECTED:
    #             try:
    #                 await connection.send_text(message)
    #                 logger.debug(f"Broadcasting: {message}")
    #             except WebSocketDisconnect as e:
    #                 print(e)
    #                 # Handle disconnection error if necessary
    #                 pass
    #         else:
    #             # Remove closed connection
    #             self.active_connections.remove(connection)

    async def broadcast(self, message: str):
        logger.debug(f"Broadcasting across {len(self.active_connections)} CONNECTIONS")
        for connection in self.active_connections:
            if connection.application_state == WebSocketState.CONNECTED:
                try:
                    await connection.send_text(message)
                    logger.debug(f"Broadcasting: {message}")
                except:
                    if connection in self.active_connections:
                        self.active_connections.remove(connection)
            else:
                if connection in self.active_connections:
                    self.active_connections.remove(connection)

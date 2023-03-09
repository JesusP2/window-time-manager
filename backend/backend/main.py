from typing import Union
from fastapi import FastAPI
from fastapi.websockets import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pynput import keyboard, mouse
from datetime import datetime
import uuid
from typing import Optional
from backend.active_window import get_active_window
from fastapi.staticfiles import StaticFiles

TIME_INTERVAL = 1
MAX_IDLE_TIME = 600
STATE = { "STATE": "Inactive" }

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    idle = {"idle_time": datetime.timestamp(datetime.now())}
    idle["idle_time"] = datetime.timestamp(datetime.now())

    def on_press(key):
        idle["idle_time"] = datetime.timestamp(datetime.now())

    def on_anything(x, y):
        idle["idle_time"] = datetime.timestamp(datetime.now())

    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_move=on_anything)
    keyboard_listener.start()  # start to listen on a separate thread
    mouse_listener.start()

    await websocket.accept()
    while True:
        msg  = await websocket.receive_text()
        print(msg)
        if msg == 'START SESSION':
            STATE['STATE'] = 'Active'
            id = uuid.uuid4().__str__()
            await websocket.send_json({
                "STATE": "START SESSION",
                "payload": {
                     "id": id, "name": "random name", "start": datetime.timestamp(datetime.now()), "end": datetime.timestamp(datetime.now()), "duration": 0, "windows": [] 
                    }
                })
        elif msg == 'FINISH SESSION':
            STATE['STATE'] = 'Inactive'
        elif msg == 'PAUSED':
            STATE['STATE'] = 'PAUSED'
        elif msg == 'DATA':
            title, app = get_active_window()
            data = {
                    "STATE": "DATA",
                    "payload": {"time": TIME_INTERVAL, "title": title, "app": app, "id": uuid.uuid4().__str__() }
                    }
            if STATE['STATE'] == 'Active':
                if datetime.timestamp(datetime.now()) - idle["idle_time"] < MAX_IDLE_TIME:
                    await websocket.send_json(data)
                else:
                    data["payload"]['title'] = "idle"
                    data["payload"]['app'] = "idle"
                    await websocket.send_json(data)
            # await asyncio.sleep(TIME_INTERVAL)


# @app.websocket("/state")
# async def state_websocket(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         print(STATE)
#         STATE['STATE'] = await websocket.receive_text()

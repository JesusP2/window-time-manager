from typing import Union
from fastapi import FastAPI
from fastapi.websockets import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pynput import keyboard, mouse
from datetime import datetime
import asyncio
from typing import Optional
from backend.active_window import get_active_window
from fastapi.staticfiles import StaticFiles

TIME_INTERVAL = 1
MAX_IDLE_TIME = 600

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
    idle = {"idle_time": 0.0}
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
        title, app = get_active_window()
        data = {"time": TIME_INTERVAL, "title": title, "app": app}
        print(data)
        if datetime.timestamp(datetime.now()) - idle["idle_time"] < MAX_IDLE_TIME:
            await websocket.send_json(data)
        await asyncio.sleep(TIME_INTERVAL)

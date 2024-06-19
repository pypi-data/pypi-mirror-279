from fastapi import APIRouter
from fastapi import FastAPI

import uvicorn
import threading

from fastapi.staticfiles import StaticFiles


class Server(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.router = APIRouter()
        self.router.add_api_route("/health", self._health, methods=["GET"])
        self.queue = {}

    def _health(self):
        return {"Status": "UP"}

    def run(self):
        app = FastAPI(openapi_url='/openapi.json',)
        app.include_router(self.router)
        app.mount("/", StaticFiles(directory="htdocs", html=True), name="htdocs")

        uvicorn.run(app, host=self.host, port=self.port)

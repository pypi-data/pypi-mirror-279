from typing import Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import threading
from koyomin.entities.user import user

server = FastAPI()

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@server.get("/oauth/callback")
async def login(code: str = Query(None)):
    user.add_user_code(code=code)
    return {"message": "Login successful!"}

class OauthServer(uvicorn.Server):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread: Optional[threading.Thread] = None

    def run_in_thread(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def shutdown_server_in_thread(self):
        if self.thread is not None:
            self.should_exit = True
            self.thread.join()

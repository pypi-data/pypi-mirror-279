from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, PlainTextResponse
from pydantic import BaseModel

from functools import wraps
import uvicorn, socket, httpx
import inspect

from concurrent.futures import ThreadPoolExecutor
import time, subprocess

import os
current_dir = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(current_dir, 'key.pub')
# print(key_path)

from typing import List, Dict
class Message(BaseModel):
    handle: str
    content: str
    history: List[Dict[str, str]]

def find_available_port(start_port):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
            port += 1

class Cycls:
    def __init__(self,network="https://cycls.com", port=find_available_port(8001),url="",debug=False):
        self.handle = None
        self.server = FastAPI()
        self.network = network
        self.port = port
        self.url = url
        self.debug = debug

    def __call__(self, handle):
        self.handle = handle
        def decorator(func):
            if inspect.iscoroutinefunction(func):
                @wraps(func)
                async def async_wrapper(*args, **kwargs):
                    return await func(*args, **kwargs)
                self.server.post('/main')(async_wrapper)
                self.publish()
                return async_wrapper
            else:
                @wraps(func)
                def sync_wrapper(*args, **kwargs):
                    return func(*args, **kwargs)
                self.server.post('/main')(sync_wrapper)
                self.publish()
                return sync_wrapper
        return decorator

    def publish(self):
        prod=False
        if self.url != "":
            prod=True

        if self.debug: print("✦/✧ debug = True")
        if prod:
            print("✦/✧","production mode",f"(url: {self.url}, port: {self.port})")
        else:
            print("✦/✧","development mode",f"(port: {self.port})")
            # self.url = f"https://{self.handle}-cycls.tuns.sh"
            self.url = f"https://{self.handle}-cycls.serveo.net"

        print("")
        print("✦/✧",f"https://cycls.com/@{self.handle}")
        print("")

        with ThreadPoolExecutor() as executor:
            if not prod:
                self.register('dev')
                executor.submit(self.tunnel)
            else:
                self.register('prod')

            if self.debug:
                executor.submit(uvicorn.run(self.server, host="127.0.0.1", port=self.port)) # perhaps keep traces?
            else:
                executor.submit(uvicorn.run(self.server, host="127.0.0.1", port=self.port, log_level="critical")) # perhaps keep traces?

    def register(self, mode):
        try:
            with httpx.Client() as client:
                response = client.post(f"{self.network}/register", json={"handle": f"@{self.handle}", "url": self.url, "mode": mode})
                if response.status_code==200:
                    print(f"✦/✧ published 🎉")
                    print("")
                else:
                    print("✦/✧ failed to register ⚠️") # exit app
        except Exception as e:
            print(f"An error occurred: {e}")

    def tunnel(self):
        # ssh_command = ['ssh', '-q', '-i', 'tuns', '-o', 'StrictHostKeyChecking=no', '-R', f'{self.handle}-cycls:80:localhost:{self.port}', 'tuns.sh']
        # ssh_command = ['ssh', '-q', '-i', 'key.pub', '-o', 'StrictHostKeyChecking=no', '-R', f'{self.handle}-cycls:80:localhost:{self.port}', 'serveo.net']
        ssh_command = ['ssh', '-q', '-i', key_path, '-o', 'StrictHostKeyChecking=no', '-R', f'{self.handle}-cycls:80:localhost:{self.port}', 'serveo.net']
        try:
            if self.debug: 
                process = subprocess.run(ssh_command,stdin=subprocess.DEVNULL) # very tricky! STDIN is what was messing with me
            else:
                process = subprocess.run(ssh_command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"An error occurred: {e}") # exit app

Text = StreamingResponse

# poetry publish --build
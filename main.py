from threading import Thread
import uvicorn
import webbrowser

from webserver import startServer
from runAPI import app


serverThread = Thread(target=startServer)
serverThread.start()

try:
    webbrowser.open('localhost:8080')
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
except KeyboardInterrupt:
    serverThread.join()
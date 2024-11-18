import os
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import subprocess

# Directory to watch
WATCH_DIR = "./build/"

def get_last_modified_time():
    """Get the most recent modification time in the directory."""
    return max(os.path.getmtime(os.path.join(root, f))
               for root, _, files in os.walk(WATCH_DIR) for f in files)

def run_server():
    """Start a simple HTTP server."""
    server = HTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)
    print("Serving on http://localhost:8000")
    server.serve_forever()

def restart_server(process):
    """Restart the server process."""
    print("Change detected, restarting server...")
    process.terminate()
    process.wait()
    return subprocess.Popen(["python3", __file__])

if __name__ == "__main__":
    print("Starting hot-reload server...")
    last_modified_time = get_last_modified_time()
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8000"])

    try:
        while True:
            time.sleep(1)
            current_modified_time = get_last_modified_time()
            if current_modified_time > last_modified_time:
                last_modified_time = current_modified_time
                server_process = restart_server(server_process)
    except KeyboardInterrupt:
        print("Shutting down server...")
        server_process.terminate()
        server_process.wait()

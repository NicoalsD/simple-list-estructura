import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from task_list import TaskList

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
TASKS = TaskList()

STATIC_TYPES = {
    ".css": "text/css",
    ".js": "application/javascript",
    ".html": "text/html",
}


class TaskRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, rel_path):
        path = os.path.normpath(os.path.join(BASE_DIR, rel_path))
        if not path.startswith(BASE_DIR) or not os.path.isfile(path):
            return self._send_json({"error": "Not found"}, 404)
        with open(path, "rb") as f:
            body = f.read()
        content_type = STATIC_TYPES.get(os.path.splitext(path)[1], "text/plain")
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html_file(self):
        self._send_file("index.html")

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length) or b"{}")

    def _task_id(self):
        parts = self.path.rstrip("/").split("/")
        try:
            return int(parts[-1])
        except (ValueError, IndexError):
            return None

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send_html_file()
        elif self.path.startswith("/static/"):
            self._send_file(self.path.lstrip("/"))
        elif self.path == "/api/tasks":
            self._send_json(TASKS.to_list())
        else:
            self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        if self.path != "/api/tasks":
            return self._send_json({"error": "Not found"}, 404)
        data = self._read_json()
        title = (data.get("title") or "").strip()
        if not title:
            return self._send_json({"error": "Title is required"}, 400)
        node = TASKS.append(title)
        self._send_json(node.to_dict(), 201)

    def do_PUT(self):
        task_id = self._task_id()
        node = TASKS.find(task_id) if task_id else None
        if node is None:
            return self._send_json({"error": "Task not found"}, 404)
        data = self._read_json()
        if "title" in data:
            title = (data.get("title") or "").strip()
            if not title:
                return self._send_json({"error": "Title is required"}, 400)
            TASKS.update(task_id, title)
        if "completed" in data:
            node.completed = bool(data["completed"])
        elif "toggle" in data:
            TASKS.toggle(task_id)
        self._send_json(node.to_dict())

    def do_DELETE(self):
        task_id = self._task_id()
        if task_id is None or not TASKS.remove(task_id):
            return self._send_json({"error": "Task not found"}, 404)
        self._send_json({"deleted": task_id})

    def log_message(self, *args):
        pass


def run(port=8000):
    server = ThreadingHTTPServer(("127.0.0.1", port), TaskRequestHandler)
    print(f"Simple Task List at http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()

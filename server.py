from flask import Flask, jsonify, render_template, request
from threading import Lock
import time

app = Flask(__name__)
lock = Lock()

# Manual motor commands for 3 robots.
# Each value is limited to -10..10.
commands = {
    "1": {"left": 0, "right": 0, "updated": 0},
    "2": {"left": 0, "right": 0, "updated": 0},
    "3": {"left": 0, "right": 0, "updated": 0},
}

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/command/<robot_id>")
def get_command(robot_id):
    robot_id = str(robot_id)
    if robot_id not in commands:
        return jsonify({"error": "robot_id must be 1, 2 or 3"}), 404

    with lock:
        data = dict(commands[robot_id])

    return jsonify({
        "robot": robot_id,
        "left": data["left"],
        "right": data["right"],
        "updated": data["updated"],
    })

@app.post("/api/command/<robot_id>")
def set_command(robot_id):
    robot_id = str(robot_id)
    if robot_id not in commands:
        return jsonify({"error": "robot_id must be 1, 2 or 3"}), 404

    body = request.get_json(silent=True) or {}
    try:
        left = max(-10, min(10, int(float(body.get("left", 0)))))
        right = max(-10, min(10, int(float(body.get("right", 0)))))
    except (TypeError, ValueError):
        return jsonify({"error": "left and right must be numbers"}), 400

    with lock:
        commands[robot_id] = {
            "left": left,
            "right": right,
            "updated": time.time(),
        }

    return jsonify({"ok": True, "robot": robot_id, "left": left, "right": right})

@app.post("/api/stop")
def stop_all():
    now = time.time()
    with lock:
        for robot_id in commands:
            commands[robot_id] = {"left": 0, "right": 0, "updated": now}
    return jsonify({"ok": True})

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)

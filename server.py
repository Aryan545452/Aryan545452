from flask import Flask, jsonify, request, render_template
from threading import Lock
import os
app=Flask(__name__)
lock=Lock()
commands={i:{"left":0,"right":0} for i in (1,2,3)}
def clamp(v):
    try:return max(-10,min(10,int(v)))
    except:return 0
@app.get("/")
def index(): return render_template("index.html")
@app.get("/api/command/<int:robot_id>")
def get_command(robot_id):
    if robot_id not in commands:return jsonify(error="robot not found"),404
    with lock:return jsonify(commands[robot_id])
@app.post("/api/command/<int:robot_id>")
def set_command(robot_id):
    if robot_id not in commands:return jsonify(error="robot not found"),404
    d=request.get_json(silent=True) or {}
    with lock:
        commands[robot_id]={"left":clamp(d.get("left",0)),"right":clamp(d.get("right",0))}
        return jsonify(ok=True,**commands[robot_id])
@app.post("/api/stop")
def stop():
    with lock:
        for i in commands: commands[i]={"left":0,"right":0}
    return jsonify(ok=True)
@app.get("/health")
def health(): return jsonify(status="ok")
if __name__=="__main__": app.run(host="0.0.0.0",port=int(os.environ.get("PORT",8000)))

from __future__ import annotations

from flask import Flask, jsonify, request

app = Flask(__name__)
state = {"last_action": None}

@app.post("/api/actuators")
def command_actuator():
    data = request.get_json(force=True)
    action = data.get("action")
    state["last_action"] = action
    print("Actuator action:", action)
    return jsonify({"status": "ok", "action": action})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

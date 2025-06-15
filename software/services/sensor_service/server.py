from __future__ import annotations

import random
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/api/sensors")
def get_sensors():
    """Return mock sensor readings."""
    moisture = random.uniform(0.0, 1.0)
    return jsonify({"moisture": moisture})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

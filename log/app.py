from datetime import datetime, timezone

from flask import Flask, jsonify, request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

app = Flask(__name__)
LOG_ATTEMPTS = Counter("log_attempts", "Liczba prob sprawdzenia hasla", ["found"])

@app.post("/log")
def log_attempt():
    data = request.get_json(silent=True) or {}
    # Tylko metadane próby - usługa log nie dostaje pełnego skrótu, hasła ani dostępu do bazy
    entry = {
        "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "hash_prefix": str(data.get("hash_prefix", ""))[:5],
        "found": bool(data.get("found")),
    }
    LOG_ATTEMPTS.labels(found="true" if entry["found"] else "false").inc()
    print(f"log: {entry}", flush=True)
    return jsonify({"status": "logged"}), 201

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

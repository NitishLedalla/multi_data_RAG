from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_URL = os.getenv("API_URL", "https://4lzdm6goqnww5ocajj6gml5bse0tuwcm.lambda-url.us-east-1.on.aws")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    try:
        r = requests.get(f"{API_URL}/health", timeout=30)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/info")
def info():
    try:
        r = requests.get(f"{API_URL}/info", timeout=30)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stats")
def stats():
    try:
        r = requests.get(f"{API_URL}/stats", timeout=30)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/documents")
def documents():
    try:
        r = requests.get(f"{API_URL}/documents", timeout=30)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files["file"]
        r = requests.post(
            f"{API_URL}/upload",
            files={"file": (file.filename, file.stream, file.content_type)},
            timeout=120
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/query", methods=["POST"])
def query():
    try:
        data = request.get_json()
        r = requests.post(
            f"{API_URL}/query",
            params={
                "question": data.get("question"),
                "auto_approve_sql": data.get("auto_approve_sql", True),
                "top_k": data.get("top_k", 3)
            },
            timeout=120
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/query/documents", methods=["POST"])
def query_documents():
    try:
        data = request.get_json()
        r = requests.post(
            f"{API_URL}/query/documents",
            params={
                "question": data.get("question"),
                "top_k": data.get("top_k", 3)
            },
            timeout=120
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/query/sql/generate", methods=["POST"])
def sql_generate():
    try:
        data = request.get_json()
        r = requests.post(
            f"{API_URL}/query/sql/generate",
            params={"question": data.get("question")},
            timeout=120
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/query/sql/execute", methods=["POST"])
def sql_execute():
    try:
        data = request.get_json()
        r = requests.post(
            f"{API_URL}/query/sql/execute",
            params={"query_id": data.get("query_id")},
            timeout=120
        )
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/query/sql/pending")
def sql_pending():
    try:
        r = requests.get(f"{API_URL}/query/sql/pending", timeout=30)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/cache/stats")
def cache_stats():
    try:
        r = requests.get(f"{API_URL}/cache/stats", timeout=30)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/cache/clear", methods=["DELETE"])
def cache_clear():
    try:
        r = requests.delete(f"{API_URL}/cache/clear", timeout=30)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/cache/query/stats")
def cache_query_stats():
    try:
        r = requests.get(f"{API_URL}/cache/query/stats", timeout=30)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/cache/query", methods=["DELETE"])
def cache_query_clear():
    try:
        r = requests.delete(f"{API_URL}/cache/query", timeout=30)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="127.0.0.1")

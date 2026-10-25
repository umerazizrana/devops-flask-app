from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    return """
    <h1>My DevOps Flask Application</h1>
    <p>Version 1 — running successfully!</p>
    <p>Git → Jenkins → Docker → Argo CD → Kubernetes</p>
    """


@app.get("/health")
def health():
    return jsonify(status="healthy"), 200

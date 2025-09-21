from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return f"Hello (plain HTTP) from tls_server container. You requested: {request.path}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

from flask import Flask, request
import sys
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return f"Hello (TLS) from tls_server container. You requested: {request.path}\n"

if __name__ == "__main__":
    # args: certfile keyfile
    if len(sys.argv) < 3:
        print("Usage: tls_server.py <certfile> <keyfile>", file=sys.stderr)
        sys.exit(1)
    certfile = sys.argv[1]
    keyfile = sys.argv[2]
    context = (certfile, keyfile)
    app.run(host="0.0.0.0", port=8443, ssl_context=context)

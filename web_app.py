import threading

import zmq
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")


def zmq_listener():
    """Listen to ZeroMQ messages and broadcast to WebSocket clients."""
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    print("ZMQ listener started, waiting for messages...")

    while True:
        try:
            message = socket.recv_string()
            message = message.strip()
            print(f"Received from ZMQ: {message}")

            # Broadcast to all connected SocketIO clients
            socketio.emit("message", {"data": message})
        except Exception as e:
            print(f"Error in ZMQ listener: {e}")
            break


@app.route("/")
def index():
    """Serve the main page."""
    return render_template("index.html")


@app.route("/message", methods=["POST"])
def send_message():
    """Send a message to all connected clients via WebSocket."""
    from flask import request

    message = request.args.get("message", "")
    if not message:
        return {"status": "error", "error": "No message provided"}, 400

    socketio.emit("message", {"data": message})
    return {"status": "success", "message": message}, 200


@socketio.on("connect")
def handle_connect():
    """Handle client connection."""
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    """Handle client disconnection."""
    print("Client disconnected")


if __name__ == "__main__":
    # Start ZMQ listener in background thread
    zmq_thread = threading.Thread(target=zmq_listener, daemon=True)
    zmq_thread.start()

    # Run Flask app with SocketIO
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)

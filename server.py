import threading
import time
from urllib.parse import quote

import requests
import zmq

WEB_APP_URL = "http://localhost:5000"

# Hardcoded playlist
PLAYLIST = [
    {"message": "Taking Back Sunday - MakeDamnSure", "duration": 5},
    {
        "message": "My Chemical Romance - Welcome to the Black Parade",
        "duration": 6,
    },
    {"message": "Dashboard Confessional - Vindicated", "duration": 4},
    {"message": "Fall Out Boy - Sugar, We're Goin Down", "duration": 5},
    {"message": "Paramore - Misery Business", "duration": 4},
    {
        "message": "Brand New - The Quiet Things That No One Ever Knows",
        "duration": 5,
    },
    {"message": "The Used - The Taste of Ink", "duration": 4},
    {
        "message": "Panic! at the Disco - I Write Sins Not Tragedies",
        "duration": 5,
    },
    {"message": "Jimmy Eat World - The Middle", "duration": 3},
    {"message": "Yellowcard - Ocean Avenue", "duration": 4},
]


def zmq_listener():
    """Secondary thread that listens for ZeroMQ messages from client."""
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://127.0.0.1:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    print("[zmq-listener] Listening for messages on tcp://127.0.0.1:5555...")

    try:
        while True:
            message = socket.recv_string()
            message = message.strip()

            print(f"[zmq-listener] Received message: {message}")

            # Send to web app
            try:
                encoded_message = quote(message)
                url = f"{WEB_APP_URL}/message?message={encoded_message}"
                response = requests.post(url)
                print(
                    f"[zmq-listener] Sent to web app: {response.status_code}"
                )
            except Exception as e:
                print(f"[zmq-listener] Error sending to web app: {e}")

    except KeyboardInterrupt:
        print("\n[zmq-listener] Shutting down...")
    finally:
        socket.close()
        context.term()


def playlist_loop():
    """Main thread that loops through the playlist."""
    print("[playlist] Starting playlist loop...")

    playlist_index = 0

    try:
        while True:
            # Get current playlist item
            item = PLAYLIST[playlist_index]
            message = item["message"]
            duration = item["duration"]

            print(f"[playlist] Now playing: {message} ({duration}s)")

            # Send to web app
            try:
                encoded_message = quote(message)
                url = f"{WEB_APP_URL}/message?message={encoded_message}"
                response = requests.post(url)
                print(f"[playlist] Sent to web app: {response.status_code}")
            except Exception as e:
                print(f"[playlist] Error sending to web app: {e}")

            # Wait for the duration
            time.sleep(duration)

            # Move to next item (loop back to start if at end)
            playlist_index = (playlist_index + 1) % len(PLAYLIST)

    except KeyboardInterrupt:
        print("\n[playlist] Shutting down...")


def main():
    """Main function that starts both threads."""
    # Start ZeroMQ listener in a separate thread
    zmq_thread = threading.Thread(target=zmq_listener, daemon=True)
    zmq_thread.start()

    # Run playlist loop in main thread
    playlist_loop()


if __name__ == "__main__":
    main()

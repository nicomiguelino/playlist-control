import asyncio
from urllib.parse import quote

import httpx
import zmq
import zmq.asyncio

WEB_APP_URL = "http://localhost:5000"


async def main():
    """Main async function that subscribes to messages."""
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://127.0.0.1:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    print(
        "Event loop is running! Waiting for messages on "
        "tcp://127.0.0.1:5555..."
    )

    async with httpx.AsyncClient() as client:
        try:
            while True:
                message = await socket.recv_string()
                message = message.strip()

                print(f"[msg-loop] Received message: {message}")

                # URL-encode the message and send to web app
                encoded_message = quote(message)
                url = f"{WEB_APP_URL}/message?message={encoded_message}"

                try:
                    response = await client.post(url)
                    print(
                        f"[msg-loop] Sent to web app: {response.status_code}"
                    )
                except Exception as e:
                    print(f"[msg-loop] Error sending to web app: {e}")

        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            socket.close()
            context.term()


if __name__ == "__main__":
    asyncio.run(main())

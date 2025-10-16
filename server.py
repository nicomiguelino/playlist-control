import asyncio

import zmq
import zmq.asyncio


async def main():
    """Main async function that subscribes to messages."""
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://127.0.0.1:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    print("Event loop is running! Waiting for messages on tcp://127.0.0.1:5555...")

    try:
        while True:
            message = await socket.recv_string()
            message = message.strip()

            if message == "previous":
                print("[msg-loop] action received: previous")
            elif message == "next":
                print("[msg-loop] action received: next")
            elif message == "pause":
                print("[msg-loop] action received: pause")
            elif message == "play":
                print("[msg-loop] action received: play")
            else:
                print(f"Unknown message: {message}")
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    asyncio.run(main())

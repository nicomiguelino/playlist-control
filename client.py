import time

import click
import zmq


@click.command()
@click.option(
    "--message",
    required=True,
    help="Message to send to the server",
)
def main(message):
    """Send a message to the ZeroMQ server."""
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://127.0.0.1:5555")

    # Give the socket time to establish connection
    time.sleep(0.1)

    socket.send_string(message)
    click.echo(f"Sent message: {message}")

    socket.close()
    context.term()


if __name__ == "__main__":
    main()

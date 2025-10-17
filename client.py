import time

import click
import zmq


@click.command()
@click.option(
    "--message",
    "-m",
    help="Message to send to the server",
)
@click.option(
    "--next",
    "command",
    flag_value="next",
    help="Skip to next track",
)
@click.option(
    "--previous",
    "-p",
    "command",
    flag_value="previous",
    help="Skip to previous track",
)
def main(message, command):
    """Send a message to the ZeroMQ server."""
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://127.0.0.1:5555")

    # Give the socket time to establish connection
    time.sleep(0.1)

    # Determine what to send
    if command:
        # Navigation command (--next or --previous)
        formatted_message = command
    elif message:
        # Regular message (--message)
        formatted_message = f"display-content {message}"
    else:
        click.echo("Error: Must provide either --message, --next, or --previous")
        socket.close()
        context.term()
        return

    socket.send_string(formatted_message)
    click.echo(f"Sent: {formatted_message}")

    socket.close()
    context.term()


if __name__ == "__main__":
    main()

# Playlist Control

A proof of concept for instant playlist navigation in digital signage systems, demonstrating interruptible playlist playback with real-time web display.

## Setup

### Initialize Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

### Start the Web App

First, start the web application server:

```bash
python web_app.py
```

The web interface will be available at `http://localhost:5000`

### Start the Playlist Server

In a separate terminal, start the playlist server:

```bash
python server.py
```

This will begin cycling through the playlist and sending updates to the web display.

### Send Commands (Optional)

Use the client to send navigation commands:

```bash
# Skip to next item
python client.py --next

# Skip to previous item
python client.py --previous

# Send custom message
python client.py --message "Your custom message"
```

## Linting & Formatting

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

### Check code

```bash
# Lint code
ruff check .

# Format code (check only)
ruff format --check .
```

### Auto-fix issues

```bash
# Fix linting issues
ruff check --fix .

# Format code
ruff format .
```

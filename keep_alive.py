import os
import random
import logging
from threading import Thread
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "I'm in!"

def run():
    port = int(os.getenv("PORT", random.randint(2000, 9000)))
    try:
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        logging.error(f"Error starting Flask server: {e}")

def keep_alive():
    """
    Creates and starts a new thread that runs the function `run`.
    """
    thread = Thread(target=run)
    thread.daemon = True  # Ensure the thread exits when the main program does
    thread.start()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    keep_alive()

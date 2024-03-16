from app import create_app
from app.ext import socketio

app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5002)
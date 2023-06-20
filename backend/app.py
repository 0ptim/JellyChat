from api import API

print("🚀 Starting server...")

app_instance = API()

# Expose the Flask app object for gunicorn.
app = app_instance.app

if __name__ == "__main__":
    app_instance.socketio.run(app_instance.app, host="0.0.0.0", port=8080)

from main import app
import os

debug = os.getenv("DEBUG", False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=debug)

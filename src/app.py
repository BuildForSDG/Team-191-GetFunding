"""The run file is used to run the entire application"""
from __init__ import app


if __name__ == "__main__":
    app.run(debug=True, port=5000)
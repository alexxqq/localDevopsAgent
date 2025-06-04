from waitress import serve
from __init__ import main

if __name__ == "__main__":
    app = main({})
    serve(app, host='0.0.0.0', port=8000)

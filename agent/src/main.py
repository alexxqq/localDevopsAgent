from waitress import serve

from service import main
from utils.logger import get_logger

logger = get_logger(__name__)

PORT = 8000

if __name__ == "__main__":
    app = main({})
    serve(app, host='0.0.0.0', port=PORT)
    logger.info(f"Started app on {PORT}")

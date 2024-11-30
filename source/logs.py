import logging
import logging.handlers


FILE_NAME = "logs.log"


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.handlers.RotatingFileHandler(FILE_NAME, maxBytes=2000, backupCount=2),
    ],
)

logger = logging.getLogger(__name__)

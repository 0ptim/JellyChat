import logging


def configure_logging():
    # Erstelle einen Logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Erstelle einen StreamHandler, um die Ausgaben in den Standardausgabestrom (stdout) zu leiten
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    # Definiere ein Format für die Log-Einträge
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)

    # Füge den StreamHandler zum Logger hinzu
    logger.addHandler(stream_handler)

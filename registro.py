"""Configuración del archivo de logs (único uso permitido de archivos)."""
import logging
import os

RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "software_fj.log")


def obtener_logger() -> logging.Logger:
    """Devuelve el logger del sistema, creándolo una sola vez."""
    os.makedirs(RUTA_LOGS, exist_ok=True)
    logger = logging.getLogger("software_fj")
    if not logger.handlers:  # evita duplicar handlers si se llama varias veces
        logger.setLevel(logging.INFO)
        manejador = logging.FileHandler(ARCHIVO_LOG, mode="w", encoding="utf-8")
        manejador.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        )
        logger.addHandler(manejador)
    return logger


log = obtener_logger()

from ddtrace import patch_all, tracer
import logging

from fk_utils import SETTINGS

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def configure_tracer():
    try:

        tracer.configure(
            https=False,
            hostname=SETTINGS.DD_HOST,
            port=SETTINGS.DD_PORT,
        )

        patch_all()

        logger.info("DDtrace tracer configurado correctamente.")

    except Exception as e:

        logger.error(f"Error al configurar el tracer de DDtrace: {e}")

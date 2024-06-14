from ddtrace import patch_all, tracer
import logging
from django.apps import AppConfig

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


class DataDogConfig(AppConfig):
    name = 'fk_utils.traces.datadog.trace'
    verbose_name = "DataDog Integration"

    def ready(self):
        configure_tracer()

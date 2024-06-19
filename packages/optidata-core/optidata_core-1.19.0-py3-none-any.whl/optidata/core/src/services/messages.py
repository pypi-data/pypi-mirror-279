import logging

from ..config import settings, constantes
from ..enums.enums import EventsLogsEnum
from ..log import AuditoryLogs
from ..utility.utils_messages import UtilsMessages

log = logging.getLogger(__name__)


def petition(json_dict):
    try:
        UtilsMessages.send_messages(settings.KAFKA_TOPIC_PETITION, json_dict)
    except Exception as ex:
        log.exception(ex)
        AuditoryLogs.registry_log(
            origin=f'{__name__}.petition',
            event=EventsLogsEnum.EVENT_ERROR,
            description=f'Error al almacenar los datos: {ex}',
            user=constantes.USER_DEFAULT
        )


def scheduler(json_dict):
    try:
        UtilsMessages.send_messages(settings.KAFKA_TOPIC_SCHEDULER, json_dict)
    except Exception as ex:
        log.exception(ex)
        AuditoryLogs.registry_log(
            origin=f'{__name__}.scheduler',
            event=EventsLogsEnum.EVENT_ERROR,
            description=f'Error al almacenar los datos: {ex}',
            user=constantes.USER_DEFAULT
        )

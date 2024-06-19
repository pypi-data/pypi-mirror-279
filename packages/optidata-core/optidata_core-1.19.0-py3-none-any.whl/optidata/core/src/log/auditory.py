from ..config import settings
from ..database import MongoAPI
from ..database.mongo_collections import MONGO_COLLECTION_AUDITORY_LOGS
from ..enums.enums import EventsLogsEnum
from ..utility import get_datetime


class AuditoryLogs:
    @staticmethod
    def registry_log(origin: str, event: EventsLogsEnum, description: str, user: str):
        data = {
            'collection': MONGO_COLLECTION_AUDITORY_LOGS,
            'Document': {
                'origin': origin,
                'event': event.value,
                'description': description,
                'user_id': user,
                'created_at': get_datetime()
            },
            'Filter': {
                'origin': origin,
                'description': description,
            }
        }

        mongodb = MongoAPI(data)
        mongodb.write(data)

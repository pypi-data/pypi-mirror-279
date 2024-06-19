import logging

from bson import ObjectId

from ..database.mongo_collections import MONGO_COLLECTION_DATA_PARTNERS
from ..database.mongodb import MongoAPI
from ..utility.utils import get_datetime, get_message_error

log = logging.getLogger(__name__)


def get_all_partners(pid: str):
    try:
        data = {
            'collection': MONGO_COLLECTION_DATA_PARTNERS,
            'Filter': {
                'active': True,
                'user_id': {
                    "$in": [pid, 'scheduler']
                }
            }
        }
        mongodb = MongoAPI(data)
        response = mongodb.all()
    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response


def new_partner(request):
    try:
        if 'id' in request:
            data = {
                'collection': MONGO_COLLECTION_DATA_PARTNERS,
                'Filter': {
                    '_id': ObjectId(request.get('id')),
                    'user_id': request.get('user_id')
                },
                'DataToBeUpdated': {
                    'name': request.get('name'),
                    'updated_at': get_datetime(),
                }
            }
            mongodb = MongoAPI(data)
            response = mongodb.update()
        else:
            data = {
                'collection': MONGO_COLLECTION_DATA_PARTNERS,
                'Document': {
                    'name': request.get('name'),
                    'user_id': request.get('user_id'),
                    'active': request.get('active'),
                    'created_at': get_datetime(),
                },
                'Filter': {
                    'name': request.get('name')
                }
            }
            mongodb = MongoAPI(data)
            response = mongodb.write(data, True)
    except Exception as e:
        log.exception(e)
        response = get_message_error(e)

    return response


def get_partner(pid: str):
    try:
        data = {
            'collection': MONGO_COLLECTION_DATA_PARTNERS,
            'Filter': {
                '_id': ObjectId(pid)
            }
        }
        mongodb = MongoAPI(data)
        response = mongodb.read()
    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response


def update_partner(pid: str, request):
    try:
        data = {
            'collection': MONGO_COLLECTION_DATA_PARTNERS,
            'Filter': {
                '_id': ObjectId(pid)
            },
            'DataToBeUpdated': {
                'name': request.get('nombre'),
                'active': request.get('activo'),
                'updated_at': get_datetime(),
            }
        }
        mongodb = MongoAPI(data)
        response = mongodb.update()
    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response


def delete_partner(pid: str):
    try:
        data = {
            'collection': MONGO_COLLECTION_DATA_PARTNERS,
            'Filter': {
                '_id': ObjectId(pid)
            }
        }
        mongodb = MongoAPI(data)
        response = mongodb.write(data)

        if response:
            data = {
                'collection': MONGO_COLLECTION_DATA_PARTNERS,
                'Filter': {
                    '_id': ObjectId(pid)
                },
                'DataToBeUpdated': {
                    'active': False,
                    'updated_at': get_datetime(),
                }
            }
            mongodb = MongoAPI(data)
            response = mongodb.update()
            if response:
                return {'Status': 'Eliminación exitosa'}

    except Exception as e:
        log.exception(e)
        response = get_message_error(e)
    return response

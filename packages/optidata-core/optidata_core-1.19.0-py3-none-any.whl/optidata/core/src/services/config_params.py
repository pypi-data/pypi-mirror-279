from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from ..config import constantes
from ..config.config_params import config_params
from ..database import MongoAPI
from ..database.mongo_collections import MONGO_COLLECTION_DATA_CONFIG_PARAMS
from ..enums.enums import EventsLogsEnum
from ..log import AuditoryLogs
from ..utility import get_datetime


def __init_set_aes_key():
    aes_key = get_random_bytes(16)
    data = {
        'collection': MONGO_COLLECTION_DATA_CONFIG_PARAMS,
        'Document': {
            'name_param': 'aes_key',
            'value_param': aes_key,
            'created_at': get_datetime()
        },
        'Filter': {
            'name_param': 'aes_key'
        }
    }
    mongodb = MongoAPI(data)
    mongodb.write(data)
    return aes_key


def set_config_params(json_dict: dict):
    data = {
        'collection': MONGO_COLLECTION_DATA_CONFIG_PARAMS,
        'Filter': {
            'name_param': 'aes_key'
        }
    }
    mongodb = MongoAPI(data)
    response = mongodb.read()
    if len(response) == 0:
        aes_key = __init_set_aes_key()
    else:
        aes_key = response[0]['value_param']

    cipher = AES.new(aes_key, AES.MODE_OCB)
    ciphertext, tag = cipher.encrypt_and_digest(json_dict.get('value_param').encode())

    response = None
    try:
        data = {
            'collection': MONGO_COLLECTION_DATA_CONFIG_PARAMS,
            'Document': {
                'type_param': json_dict.get('type_param'),
                'name_param': json_dict.get('name_param'),
                'tag_param': tag,
                'nonce_param': cipher.nonce,
                'text_param': ciphertext,
                'created_date': get_datetime()
            },
            'Filter': {
                'type_param': json_dict.get('type_param'),
                'name_param': json_dict.get('name_param')
            },
            'DataToBeUpdated': {
                'tag_param': tag,
                'nonce_param': cipher.nonce,
                'text_param': ciphertext,
                'updated_date': get_datetime()
            }
        }

        mongodb = MongoAPI(data)
        response = mongodb.write(data)
    except Exception as ex:
        AuditoryLogs.registry_log(
            origin=f'{__name__}.set_config_params',
            event=EventsLogsEnum.EVENT_ERROR,
            description=f'Error al obtener los datos: {ex}',
            user=constantes.USER_DEFAULT
        )

    return response


def get_config_params(p, t):
    json_dict = {
        'name_param': p,
        'type_param': t
    }

    response = None
    data = {
        'collection': MONGO_COLLECTION_DATA_CONFIG_PARAMS,
        'Filter': {
            'name_param': 'aes_key'
        }
    }
    mongodb = MongoAPI(data)
    result = mongodb.read()
    if len(result) == 0:
        aes_key = __init_set_aes_key()
    else:
        aes_key = result[0]['value_param']

    try:
        data = {
            'collection': MONGO_COLLECTION_DATA_CONFIG_PARAMS,
            'Filter': {
                'name_param': json_dict.get('name_param'),
                'type_param': json_dict.get('type_param')
            }
        }

        mongodb = MongoAPI(data)
        response = mongodb.read()
        if len(response) > 0:
            key = dict(response[0])
            ciphertext = key.get('text_param')
            tag = key.get('tag_param')
            nonce = key.get('nonce_param')

            cipher = AES.new(aes_key, AES.MODE_OCB, nonce=nonce)
            try:
                message = cipher.decrypt_and_verify(ciphertext, tag)
                response = message.decode()
            except ValueError as ex:
                AuditoryLogs.registry_log(
                    origin=f'{__name__}.get_config_params',
                    event=EventsLogsEnum.EVENT_ERROR,
                    description=f'Error al obtener los datos: {ex}',
                    user=constantes.USER_DEFAULT
                )
        else:
            AuditoryLogs.registry_log(
                origin=f'{__name__}.get_config_params',
                event=EventsLogsEnum.EVENT_ERROR,
                description=f'El parámetro {json_dict.get("name_param")} no existe',
                user=constantes.USER_DEFAULT
            )

    except Exception as ex:
        AuditoryLogs.registry_log(
            origin=f'{__name__}.get_config_params',
            event=EventsLogsEnum.EVENT_ERROR,
            description=f'Error al obtener los datos: {ex}',
            user=constantes.USER_DEFAULT
        )

    return response


def get_all_config_params_by_type(t):
    response_data = None
    try:
        data = {
            'collection': MONGO_COLLECTION_DATA_CONFIG_PARAMS,
            'Filter': {
                'name_param': 'aes_key'
            }
        }
        mongodb = MongoAPI(data)
        result = mongodb.read()
        if len(result) == 0:
            aes_key = __init_set_aes_key()
        else:
            aes_key = result[0]['value_param']

        data_type = config_params.get(t)
        if len(data_type) > 0:
            data = {
                'collection': MONGO_COLLECTION_DATA_CONFIG_PARAMS,
                'Filter': {
                    'type_param': t
                }
            }

            mongodb = MongoAPI(data)
            response = mongodb.read()
            if len(response) > 0:
                response_data = {
                    'conf': t,
                    'data': {}
                }
                for key in response:
                    ciphertext = key.get('text_param')
                    tag = key.get('tag_param')
                    nonce = key.get('nonce_param')

                    cipher = AES.new(aes_key, AES.MODE_OCB, nonce=nonce)
                    try:
                        dict_response = [d for d in data_type if key.get('name_param') in d.values()][0]

                        key_list = list(dict_response.keys())
                        val_list = list(dict_response.values())
                        position = val_list.index(key.get('name_param'))

                        message = cipher.decrypt_and_verify(ciphertext, tag)
                        response_data['data'][f'{key_list[position]}'] = message.decode()
                    except ValueError as ex:
                        AuditoryLogs.registry_log(
                            origin=f'{__name__}.get_all_config_params_by_type',
                            event=EventsLogsEnum.EVENT_ERROR,
                            description=f'Error al obtener los datos: {ex}',
                            user=constantes.USER_DEFAULT
                        )
            else:
                response_data = []
                AuditoryLogs.registry_log(
                    origin=f'{__name__}.get_all_config_params_by_type',
                    event=EventsLogsEnum.EVENT_ERROR,
                    description=f'El tipo parámetro {t} no existe',
                    user=constantes.USER_DEFAULT
                )
        else:
            AuditoryLogs.registry_log(
                origin=f'{__name__}.get_all_config_params_by_type',
                event=EventsLogsEnum.EVENT_ERROR,
                description=f'El tipo parámetro {t} no existe',
                user=constantes.USER_DEFAULT
            )

    except Exception as ex:
        AuditoryLogs.registry_log(
            origin=f'{__name__}.get_all_config_params_by_type',
            event=EventsLogsEnum.EVENT_ERROR,
            description=f'Error al obtener los datos: {ex}',
            user=constantes.USER_DEFAULT
        )

    return response_data

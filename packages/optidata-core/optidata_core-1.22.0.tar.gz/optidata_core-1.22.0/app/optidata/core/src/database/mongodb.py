import json
from datetime import datetime

import chardet
import pymongo
from pymongo import MongoClient

from .mongo_collections import MONGO_COLLECTION_PROC_RECONCILED_CNF, MONGO_COLLECTIONS, \
    MONGO_COLLECTION_DATA_CONFIG_PARAMS
from .mongo_settings import MONGO_DB_USER, MONGO_DB_NAME, MONGO_DB_PORT, MONGO_DB_HOST, MONGO_DB_PWD, MONGO_DB_URI
from ..config import constantes

# Configuración del cursor para obtener los datos en lotes
size_lote = constantes.MONGO_BATCH_SIZE  # Número de documentos por lote


class MongoAPI:
    def __init__(self, data=None):
        self.total_data = 0
        self.offset = 20
        self.limit = 10

        self.starting_id = ''
        self.last_id = ''

        if MONGO_DB_USER == '':
            self.client = MongoClient(
                MONGO_DB_URI,
                compressors='zlib',
                directConnection=True
            )
        else:
            self.client = MongoClient(
                host=f'{MONGO_DB_HOST}:{MONGO_DB_PORT}',
                username=MONGO_DB_USER,
                password=MONGO_DB_PWD,
                # replicaset='dbrs',
                compressors='zlib',
                directConnection=True
            )

        if MONGO_DB_NAME not in self.client.list_database_names():
            self.db = self.client[f'{MONGO_DB_NAME}']
        else:
            self.db = self.client.get_database(f'{MONGO_DB_NAME}')

        if data:
            if 'collection' in data:
                self.collection = self.db[data['collection']]
            self.data = data

    def check_collections(self, custom_collections=None):
        collections = custom_collections if custom_collections else MONGO_COLLECTIONS
        for collection in collections:
            if collection not in self.db.list_collection_names():
                self.db.create_collection(collection)

    def read(self):
        """
        Retorna el documento disponible en base a filtro, ordenado y/o agrupado
        :return:
        """
        return self.__search_documents(
            self.data['Filter'] if 'Filter' in self.data else None,
            self.data['Sort'] if 'Sort' in self.data else None,
            self.data['Group'] if 'Group' in self.data else None,
            self.data['Columns'] if 'Columns' in self.data else None
        )

    def all(self):
        """
        Retorna todos los documentos disponibles a ser procesados basándose en filtros, ordenado y/o agrupado
        :return:
        """
        return self.__search_documents(
            self.data['Filter'] if 'Filter' in self.data else None,
            self.data['Sort'] if 'Sort' in self.data else None,
            self.data['Group'] if 'Group' in self.data else None,
            self.data['Columns'] if 'Columns' in self.data else None
        )

    def write(self, data, force_new=False):
        """
        Función que permite insertar un nuevo Documento en caso de no existir en la BD Mongo
        :param data:
        :param force_new
        :return: list[Mapping[str, Any]]
        """
        output = self.read()
        if output and not force_new:
            document_id = str(output[0]['_id'])
            self.update()
        else:
            new_document = data['Document']
            response = self.collection.insert_one(new_document)
            document_id = str(response.inserted_id)

        output = {'Status': 'Creación exitosa', 'Document_ID': document_id}
        return output

    def write_many(self, documents):
        """
        Función que permite insertar un nuevo Documento en caso de no existir en la BD Mongo
        :param documents:
        :return: list[Mapping[str, Any]]
        """
        output = self.read()
        if output:
            document_id = str(output[0]['_id'])
        else:
            response = self.collection.insert_many(documents)
            document_id = str(response.inserted_ids)

        output = {'Status': 'Creación exitosa', 'Document_ID': document_id}
        return output

    def update(self):
        """
        Función que actualiza la información en la BD Mongo
        :return: dict[str, str]
        """
        if 'DataToBeUpdated' in self.data:
            _filter = self.data['Filter']
            updated_data = {"$set": self.data['DataToBeUpdated']}
            response = self.collection.update_one(_filter, updated_data)
            output = {
                'Status': 'Actualización exitosa' if response.modified_count > 0 else "No hay nada que actualizar."}
            return output
        return None

    def delete(self, data):
        """
        Elimina lógicamente un registro desde la BD Mongo
        :param data:
        :return:
        """
        _filter = data['Filter']
        response = self.collection.delete_one(_filter)
        output = {'Status': 'Eliminación exitosa' if response.deleted_count > 0 else "Documento no encontrado."}
        return output

    def delete_many(self, data):
        """
        Elimina lógicamente un registro desde la BD Mongo
        :param data:
        :return:
        """
        _filter = data['Filter']
        response = self.collection.delete_many(_filter)
        output = {'Status': 'Eliminación exitosa' if response.deleted_count > 0 else "Documento no encontrado."}
        return output

    def read_with_pagination(self, data):
        _filter = data['Filter']
        output = []
        self.total_data = self.collection.count_documents(_filter)
        if self.total_data > 0:
            self.offset = int(data['Pagination']['offset'])  # corresponde al item que inicia el resultado obtenido
            if self.offset > self.total_data:
                self.offset = self.total_data

            self.limit = int(data['Pagination']['limit'])  # corresponde a la cantidad de datos devueltos
            self.starting_id = self.collection.find(_filter).sort('_id', pymongo.ASCENDING)
            self.last_id = self.starting_id[self.offset - 1]['_id']

            documents = self.collection.find({"$and": [_filter, {'_id': {'$gte': self.last_id}}]}) \
                .sort('_id', pymongo.ASCENDING) \
                .limit(self.limit)

            for document in documents:
                document['_id'] = str(document['_id'])
                del document[f'{MONGO_COLLECTION_PROC_RECONCILED_CNF}_id']
                output.append(document)

        next_offset = self.offset + self.limit
        prev_offset = self.offset - self.limit
        return {
            'next': next_offset,
            'prev': prev_offset if prev_offset > 0 else 1,
            'data': output,
            'total': self.total_data
        }

    def __search_documents(self, _filter=None, _sort=None, _group=None, _cols=None):
        if _filter is None:
            _filter = {}
        else:
            columns_filter = ''
            init = True
            for key, value in _filter.items():
                if init:
                    columns_filter = f"{key}"
                    init = False
                else:
                    columns_filter += f",{key}"
            self.collection.create_index(columns_filter)

        output = []

        if _group:
            self.collection.aggregate(
                [{
                    '$group': _group
                }]
            )

        lote_actual = 0
        total_datos = self.collection.count_documents(_filter)
        while lote_actual < total_datos:
            if _sort:
                lote = self.collection.find(_filter, _cols if _cols else {}).skip(lote_actual).limit(size_lote).sort(_sort)
            else:
                lote = self.collection.find(_filter, _cols if _cols else {}).skip(lote_actual).limit(size_lote)

            for documento in lote:
                documento['_id'] = str(documento['_id'])
                if self.data['collection'] != MONGO_COLLECTION_DATA_CONFIG_PARAMS:
                    for param in ['created_at', 'deleted_at']:
                        if param in documento:
                            documento = json.loads(json.dumps(documento, cls=DateTimeEncoder, ensure_ascii=False))
                output.append(documento)

            lote_actual += size_lote
        return output


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime):
            return str(z)
        else:
            return super().default(z)

import logging
import platform
import traceback

import oracledb
from oracledb import DatabaseError
from sqlalchemy import create_engine, NullPool
from sqlalchemy.orm import sessionmaker

from ..config import settings

log = logging.getLogger(__name__)

d = None  # default suitable for Linux
f = None
if platform.system() == 'Darwin' and platform.machine() == 'x86_64':  # macOS
    d = 'linux'
    f = '/optidata'
elif platform.system() == 'Windows':
    d = 'win'
    f = 'c:'

if d and f:
    oracledb.init_oracle_client(lib_dir=f'{f}/oracle_client/{d}')
else:
    oracledb.init_oracle_client()


log = logging.getLogger(__name__)


class OracleAPI:
    def __init__(self, show_sql=False):
        try:
            if settings.ORACLE_SERVICE_NAME != '':
                cp = oracledb.ConnectParams(
                    host=f'{settings.ORACLE_HOST}',
                    port=int(settings.ORACLE_PORT),
                    sid=f'{settings.ORACLE_SERVICE_NAME}',
                    user=settings.ORACLE_USERNAME,
                    password=settings.ORACLE_PASSWORD
                )
            elif settings.ORACLE_DB_NAME != '':
                cp = oracledb.ConnectParams(
                    host=f'{settings.ORACLE_HOST}',
                    port=int(settings.ORACLE_PORT),
                    service_name=f'{settings.ORACLE_DB_NAME}',
                    user=settings.ORACLE_USERNAME,
                    password=settings.ORACLE_PASSWORD
                )

            dsn = cp.get_connect_string()

            self.pool = oracledb.create_pool(
                user=settings.ORACLE_USERNAME,
                password=settings.ORACLE_PASSWORD,
                dsn=dsn,
                min=1,
                max=4,
                increment=1,
                disable_oob=True,
                ping_interval=2,
                getmode=oracledb.POOL_GETMODE_WAIT
            )

            self.engine = create_engine(
                f'oracle+oracledb://:@',
                creator=self.pool.acquire,
                poolclass=NullPool,
                echo=show_sql,
                thick_mode=False,
                connect_args={
                    'user': settings.ORACLE_USERNAME,
                    'password': settings.ORACLE_PASSWORD,
                    'host': settings.ORACLE_HOST,
                    'port': settings.ORACLE_PORT,
                    'service_name': settings.ORACLE_DB_NAME,
                    'dsn': dsn,
                    'dbname': settings.ORACLE_SCHEMA,
                    'schema': settings.ORACLE_SCHEMA,
                    'options': f'-csearch_path={settings.ORACLE_SCHEMA}'
                }
            )

            # Create a session to the database
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

        except DatabaseError:
            log.exception("Couldn't connect to Oracle DataBase.", {'ex': traceback.format_exc()})

    def read(self, sql):
        try:
            result = self.session.execute(sql).fetchone()
        except Exception as ex:
            log.exception(ex)
            result = []
        return result if len(result) > 0 else []

    def all(self, sql):
        try:
            result = self.session.execute(sql).fetchall()
        except Exception as ex:
            log.exception(ex)
            result = []
        return result if len(result) > 0 else []

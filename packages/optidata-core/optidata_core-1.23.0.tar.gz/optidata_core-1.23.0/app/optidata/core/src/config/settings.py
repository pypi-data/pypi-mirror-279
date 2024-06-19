# Version liberación - Release ddmmyyyy
from ..services.config_params import get_config_params

APP_VERSION = '1.23.0'
# Flask Settings
FLASK_SECRET_KEY = '0pt1m1$42560-$3cr3t4'

FLASK_DEBUG = True
FLASK_THREADED = True
FLASK_ERROR_404_HELP = False
FLASK_APP_FOLDER = 'optidata-core'
FLASK_NAME_UPLOAD_FOLDER = 'files'
FLASK_NAME_EXPORT_FOLDER = 'exported-files'
FLASK_ALLOWED_EXTENSIONS = {'txt', 'csv', 'xls', 'xlsx'}
FLASK_MAX_CONTENT_LENGTH = 500 * 1024 * 1024
FLASK_NUMBER_PROCESSES = 2
FLASK_ROOT_PATH = ''
FLASK_UPLOAD_FOLDER = ''
FLASK_EXPORT_FOLDER = ''

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False
RESTPLUS_API_VERSION = '/v1'
RESTPLUS_EMPTY_RESULT = 'No existen registros asociados'

# Oracle Properties (SAP)
ORACLE_HOST = get_config_params('ORACLE_HOST', 'database')
ORACLE_PORT = get_config_params('ORACLE_PORT', 'database')
ORACLE_USERNAME = get_config_params('ORACLE_USER', 'database')
ORACLE_PASSWORD = get_config_params('ORACLE_PWD', 'database')
ORACLE_DB_NAME = get_config_params('ORACLE_DB', 'database')
ORACLE_SERVICE_NAME = get_config_params('ORACLE_SID', 'database')
ORACLE_SCHEMA = get_config_params('ORACLE_SCHEMA', 'database')
ORACLE_ENCODING = 'UTF-8'

# BCrypt Config
BCRYPT_LOG_ROUNDS = 13

# JWT Configuration
TOKEN_EXPIRE_HOURS = 1
TOKEN_EXPIRE_MINUTES = 15
TOKEN_REFRESH_EXPIRE_HOURS = 1
TOKEN_HEADER_NAME = 'X-Access-Token'
TOKEN_FORMAT = 'Bearer '

# Files Configuration
FILE_EXT_TXT = 'txt'
FILE_EXT_CSV = 'csv'
FILE_EXT_XLS = 'xls'
FILE_EXT_XLSX = 'xlsx'
CSV_SEPARATOR = ';'

# Vaex Configuration
VAEX_THREAD_COUNT = 10
VAEX_MAX_COLUMN = 10000

# Default Configurations - User/Role
DEFAULT_USERNAME = 'admin@optimisa.cl'
DEFAULT_PASSWORD = ''
DEFAULT_FIRSTNAME = 'Administrador'
DEFAULT_LASTNAME = 'del Sistema'

DEFAULT_USER_USERNAME = 'consulta@optimisa.cl'
DEFAULT_USER_PASSWORD = ''
DEFAULT_USER_FIRSTNAME = 'Usuario Consulta'
DEFAULT_USER_LASTNAME = 'del Sistema'

DEFAULT_ROLE_NAME_ADMIN = 'Administrador'
DEFAULT_ROLE_NAME_USER = 'Consulta'

# Kafka Properties
KAFKA_BOOSTRAP = get_config_params('KAFKA_SERVER', 'kafka')
KAFKA_PORT = get_config_params('KAFKA_PORT', 'kafka')
KAFKA_SASL_MECHANISM = 'PLAIN'
KAFKA_SECURITY_PROTOCOL = 'SASL_SSL'
KAFKA_USERNAME = get_config_params('KAFKA_USER', 'kafka')
KAFKA_PASSWORD = get_config_params('KAFKA_PWD', 'kafka')
KAFKA_OFFSET = 'earliest'
KAFKA_TIMEOUT = 1000
KAFKA_ENCODE = 'UTF-8'

KAFKA_CONSUMER_COMMIT_INTERVAL_MS = 5000
KAFKA_CONSUMER_TIMEOUT = 50
KAFKA_CONSUMER_FETCH_MESSAGE_MAX_BYTES = 10 * 1024 * 1024  # 10MB
KAFKA_CONSUMER_AUTO_COMMIT_ENABLE = True

# Kafka Topics
KAFKA_TOPIC_SCHEDULER = 'topic_schedulers'
KAFKA_TOPIC_PETITION = 'topic-requeriments'

# SFTP Properties
SFTP_HOSTNAME = get_config_params('SFTP_HOST', 'sftp')
SFTP_PORT = get_config_params('SFTP_PORT', 'sftp')
SFTP_USERNAME = get_config_params('SFTP_USER', 'sftp')
SFTP_PASSWORD = get_config_params('SFTP_PWD', 'sftp')
SFTP_PATH_DEFAULT = 'sftp'

# Scheduler Properties
SCHEDULER_MIN_TIME_RUN = 1
SCHEDULER_MIN_TIME_RUN_LOTES = 1
SCHEDULER_MIN_TIME_RUN_CARTOLA = 1
SCHEDULER_MIN_TIME_RUN_PA = 1

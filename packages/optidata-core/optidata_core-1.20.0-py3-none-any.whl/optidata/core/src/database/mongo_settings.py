# MongoDB Configuration
MONGO_BATCH_SIZE = 100000
MONGO_DB_HOST = '172.20.3.37'  # get_config_params('DB_HOST')
MONGO_DB_PORT = '27027'  # get_config_params('DB_PORT')
MONGO_DB_NAME = 'optidata_db'
MONGO_DB_URI = f'mongodb://{MONGO_DB_HOST}:{MONGO_DB_PORT}/{MONGO_DB_NAME}'
MONGO_DB_USER = 'admin@optimisa.cl'  # get_config_params('DB_USER')
MONGO_DB_PWD = '0pt1m1542560_2024'  # get_config_params('DB_PWD')

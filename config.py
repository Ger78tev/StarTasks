import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'startask_railway_production_secret_key_2024')
    
    # Usar variables MYSQL* de Railway (se crean automáticamente)
    DB_HOST = os.environ.get('MYSQLHOST', 'localhost')
    DB_USER = os.environ.get('MYSQLUSER', 'root')
    DB_PASSWORD = os.environ.get('MYSQLPASSWORD', '')
    DB_NAME = os.environ.get('MYSQLDATABASE', 'startask')
    DB_PORT = os.environ.get('MYSQLPORT', '3306')
    
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}

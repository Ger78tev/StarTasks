import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'startask_railway_postgres_secret_2024')
    
    # Configuración para PostgreSQL en Railway
    DB_HOST = os.environ.get('PGHOST', 'localhost')
    DB_USER = os.environ.get('PGUSER', 'postgres')
    DB_PASSWORD = os.environ.get('PGPASSWORD', '')
    DB_NAME = os.environ.get('PGDATABASE', 'startask')
    DB_PORT = int(os.environ.get('PGPORT', 5432))
    
    # Configuración Flask
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}

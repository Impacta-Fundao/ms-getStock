import os
from dotenv import load_dotenv
load_dotenv()

class Config_db:
        
    DB_USER = os.getenv('DEV_DB_USER')
    DB_PASS= os.getenv('DEV_DB_PASS')
    DB_HOST= os.getenv('DEV_DB_HOST')
    DB_PORT= os.getenv('DEV_DB_PORT')
    DB_NAME= os.getenv('DEV_DB_NAME')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

class Config_db_hml:
    
    DB_USER = os.getenv('HML_DB_USER')
    DB_PASS= os.getenv('HML_DB_PASS')
    DB_HOST= os.getenv('HML_DB_HOST')
    DB_PORT= os.getenv('HML_DB_PORT')
    DB_NAME= os.getenv('HML_DB_NAME')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

class Config_db_prd:
    
    DB_USER = os.getenv('PRD_DB_USER')
    DB_PASS= os.getenv('PRD_DB_PASS')
    DB_HOST= os.getenv('PRD_DB_HOST')
    DB_PORT= os.getenv('PRD_DB_PORT')
    DB_NAME= os.getenv('PRD_DB_NAME')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    

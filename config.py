import os

class Config:
    DB_USERNAME = os.environ.get("MYSQLUSER", "root")          
    DB_PASSWORD = os.environ.get("MYSQLPASSWORD", "Prime")     
    DB_HOST = os.environ.get("MYSQLHOST", "localhost")         
    DB_NAME = os.environ.get("MYSQLDATABASE", "smartest")      
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

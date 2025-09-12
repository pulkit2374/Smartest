import os

class Config:
    DB_USERNAME = os.environ.get("MYSQLUSER", "root")          
    DB_PASSWORD = os.environ.get("MYSQLPASSWORD", "DzZFgVkFDzXTzeHwdhavteVdGxjUBEEW")     
    DB_HOST = os.environ.get("MYSQLHOST", "mysql.railway.internal")         
    DB_NAME = os.environ.get("MYSQLDATABASE", "railway")      
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{root}:{DzZFgVkFDzXTzeHwdhavteVdGxjUBEEW}@{mysql.railway.internal}/{railway}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

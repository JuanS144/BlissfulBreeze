"""
    This is the config.py class that contains all configurations,
    database server credentials and the SECRET_KEY which will all be 
    used by app
"""
import secrets as scr
import os

class Config:
    """
        This is the Config class that will initialize all configurations,
        database server credentials and the SECRET_KEY which will all be 
        used by app    
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', scr.token_hex(16))
    DB_HOST = 'dc303.dawsoncollege.qc.ca'
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_PORT = os.environ.get('DB_PORT')
    
# export DB_NAME=server_side_2338205

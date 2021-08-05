from flask_sqlalchemy import SQLAlchemy

class DBConnector():

    db=None

    def __init__(self) -> None:
        pass


    @staticmethod
    def InitConnection(app):
        global db
       

        db = SQLAlchemy(app)
        
    @staticmethod
    def getDB():
        global db
        return db
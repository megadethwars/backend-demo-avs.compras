from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields,schema,validates,Schema
from sqlalchemy import Column

from ..DBConnector import DBConnector
#db = DBConnector.getDB()
db=DBConnector.getDB()


class RoleModel(db.Model):

    __tablename__ ="roles"

    id = db.Column(db.Integer,primary_key=True)
    cargo = db.Column(db.String(70))
 
    def __init__(self,data):
        self.cargo=data.get("cargo")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self,data):
        for key,item in data.items():
            setattr(self,key,item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        try:
            return RoleModel.query.all()
        except:
            print('error')

    @staticmethod
    def get_by_id(id):
        return RoleModel.query.get(id)

    @staticmethod
    def get_by_name(id):
        return RoleModel.query.filter_by(cargo=id).first()

    def __repr(self):
        return "<id {}>".format(self.id)

class Roleschema(Schema):
    id = fields.Int()
    cargo=fields.String()

class RoleschemaIn(Schema):
    cargo=fields.String()
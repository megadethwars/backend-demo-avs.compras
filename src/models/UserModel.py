from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields,schema,validates,Schema
from sqlalchemy import Column
import datetime

from ..DBConnector import DBConnector
#db = DBConnector.getDB()
db=DBConnector.getDB()


class UserModel(db.Model):

    __tablename__ ="usuarios"

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(70))
    nombre = db.Column(db.String(70))
    password = db.Column(db.String(70))
    efectivo = db.Column(db.Integer)
    rol = db.Column(db.Integer,db.ForeignKey("roles.id"),nullable = False)
    fechaCreacion = db.Column(db.DateTime)
    perfil = db.Column(db.LargeBinary(length=(2**32)-1))
 
    def __init__(self,data,blob):
    
        self.username = data.get("username")
        self.nombre = data.get("nombre")
        self.password = data.get("password")
        self.efectivo = data.get("efectivo")
        self.rol = data.get("rol")
        self.fechaCreacion = datetime.datetime.now()
        self.perfil = blob

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
            return UserModel.query.all()
        except:
            print('error')

    @staticmethod
    def get_by_id(id):
        return UserModel.query.get(id)

    @staticmethod
    def get_by_name(id):
        return UserModel.query.filter_by(username=id).first()

    def __repr(self):
        return "<id {}>".format(self.id)

class Userschema(Schema):
    id = fields.Int()
    username = fields.String()
    nombre = fields.String()
    password = fields.String()
    efectivo = fields.Int()
    rol = fields.Int()
    perfil = fields.String()
    fechaCreacion = fields.DateTime()

class UserschemaIn(Schema):
    username = fields.String()
    nombre = fields.String()
    password = fields.String()
    efectivo = fields.Int()
    rol = fields.Int()
    fechaCreacion = fields.DateTime()
    perfil = fields.String()
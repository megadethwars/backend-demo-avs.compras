from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields,schema,validates,Schema
from sqlalchemy import Column
import datetime

from ..DBConnector import DBConnector
#db = DBConnector.getDB()
db=DBConnector.getDB()


class ProductsModel(db.Model):

    __tablename__ ="products"

    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(70))
    descripcion = db.Column(db.String(200))
    marca = db.Column(db.String(70))
    precio = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    fechaCreacion = db.Column(db.DateTime)
    perfil = db.Column(db.LargeBinary(length=(2**32)-1))
 
    def __init__(self,data,blob):
    
        self.nombre = data.get("nombre")
        self.descripcion = data.get("descripcion")
        self.marca = data.get("marca")
        self.precio = data.get("precio")
        self.cantidad = data.get("cantidad")
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
            return ProductsModel.query.all()
        except:
            print('error')

    @staticmethod
    def get_by_id(id):
        return ProductsModel.query.get(id)

    @staticmethod
    def get_by_name(id):
        return ProductsModel.query.filter_by(nombre=id).first()

    def __repr(self):
        return "<id {}>".format(self.id)

class Productschema(Schema):
    id = fields.Int()
    nombre = fields.String()
    descripcion = fields.String()
    marca = fields.String()
    precio = fields.Int()
    cantidad = fields.Int()
    perfil = fields.String()
    fechaCreacion = fields.DateTime()

   

class ProductschemaIn(Schema):
    nombre = fields.String()
    descripcion = fields.String()
    marca = fields.String()
    password = fields.String()
    efectivo = fields.Int()
    precio = fields.Int()
    cantidad = fields.Int()
    perfil = fields.String()
    fechaCreacion = fields.DateTime()
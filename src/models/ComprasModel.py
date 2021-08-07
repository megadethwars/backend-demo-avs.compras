from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields,schema,validates,Schema
from sqlalchemy import Column
import datetime

from ..DBConnector import DBConnector
#db = DBConnector.getDB()
db=DBConnector.getDB()


class ComprasModel(db.Model):

    __tablename__ ="compras"

    id = db.Column(db.Integer,primary_key=True)
    usuario = db.Column(db.Integer,db.ForeignKey("usuarios.id"),nullable = False)
    producto = db.Column(db.Integer,db.ForeignKey("products.id"),nullable = False)
    fechaCreacion = db.Column(db.DateTime)
    
 
    def __init__(self,data):
    
        self.usuario = data.get("usuario")
        self.producto = data.get("producto")
        self.fechaCreacion = datetime.datetime.now()

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
            return ComprasModel.query.all()
        except:
            print('error')

    @staticmethod
    def get_by_id(id):
        return ComprasModel.query.get(id)

    @staticmethod
    def get_by_name(id):
        return ComprasModel.query.filter_by(username=id).first()

    @staticmethod
    def get_by_producto(id):
        return ComprasModel.query.filter_by(producto=id).first()

    @staticmethod
    def get_by_usuario(id):
        return ComprasModel.query.filter_by(usuairo=id).first()

    @staticmethod
    def del_by_producto(id):
        return ComprasModel.query.filter_by(producto=id).delete()

    @staticmethod
    def del_by_usuario(id):
        return ComprasModel.query.filter_by(usuairo=id).delete()

    @staticmethod
    def get_by_query(data):
        return ComprasModel.query.filter_by(**data).all()

    def __repr(self):
        return "<id {}>".format(self.id)

class Compraschema(Schema):
    id = fields.Int()
    usuario = fields.Int()
    producto = fields.Int()
    fechaCreacion = fields.DateTime()
    

class CompraschemaIn(Schema):
    usuario = fields.Int(required=True)
    producto = fields.Int(required=True)
    
class ComprasQuerySchema(Schema):
    filtros = fields.Dict()


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
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
    cantidad = db.Column(db.Integer)
    fechaCreacion = db.Column(db.DateTime)
    
 
    def __init__(self,data):
    
        self.usuario = data.get("usuario")
        self.producto = data.get("producto")
        self.cantidad = data.get("cantidad")
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
        return ComprasModel.query.filter_by(usuario=id).first()

    @staticmethod
    def del_by_producto(id):
        return ComprasModel.query.filter_by(producto=id).delete()

    @staticmethod
    def del_by_usuario(id):
        return ComprasModel.query.filter_by(usuario=id).delete()

    @staticmethod
    def get_by_query(data):
        return ComprasModel.query.filter_by(**data).all()

    
    @staticmethod
    def get_all_by_page(page,per_page):
        return ComprasModel.query.order_by(ComprasModel.fechaCreacion.desc()).paginate(page,per_page,error_out=False)

    def __repr(self):
        return "<id {}>".format(self.id)

class Compraschema(Schema):
    id = fields.Int()
    usuario = fields.Int()
    producto = fields.Int()
    cantidad = fields.Int()
    fechaCreacion = fields.DateTime()
    

class CompraschemaIn(Schema):
    usuario = fields.Int(required=True)
    producto = fields.Int(required=True)
    cantidad = fields.Int(required=True)
    fechaCreacion = fields.DateTime()
    
class ComprasQuerySchema(Schema):
    filtros = fields.Dict()


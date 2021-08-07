from src.models.ProductsModel import ProductsModel, Productschema
from src.utilities import ReturnCodes
from src import utilities
from flask import Flask,request,Response,jsonify,json,Blueprint
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields,schema,validates,Schema
from sqlalchemy import Column

from ..models.UserModel import UserModel,Userschema,UserschemaIn,UserschemaUpCash
from ..models.ComprasModel import Compraschema,CompraschemaIn,ComprasModel,ComprasQuerySchema
from ..utilities import ReturnCodes
from ..DBConnector import DBConnector
import traceback

db=DBConnector.getDB()
compra_schema =Compraschema()
compra_schemaIn = CompraschemaIn()
compra_query_schema=ComprasQuerySchema()
user_schema = Userschema()
product_schema= Productschema()
user_schema_cash = UserschemaUpCash()

compra_api = Blueprint("compra_api",__name__)

@compra_api.route("",methods=["POST"])
def create():
    

    try:
        req_data = request.get_json()
        data = compra_schemaIn.load(req_data)

        #check if user exist
        rol = UserModel.get_by_id(req_data['usuario'])

        if not rol:
            return ReturnCodes.custom_response({},409,"el usuario no existe")

        producto = ProductsModel.get_by_id(req_data['producto'])
        if not producto:
            return ReturnCodes.custom_response({},409,"el producto no existe")

        #check if stock is available
        if producto.cantidad<1:
            return ReturnCodes.custom_response({},409,"no hay cantidad suficiente para comprar el producto "+producto.nombre)

        #check is user money is available
        if rol.efectivo<1:
            return ReturnCodes.custom_response({},409,"el usuario" +rol.username+"no tiene efectivo para realizar una compra")
        
        #check is user has enought money to pay
        if rol.efectivo<producto.cantidad:
            return ReturnCodes.custom_response({},409,"el usuario"+rol.username+"no tiene efectivo suficiente para realizar una compra")

        compra = ComprasModel(data)
        compra.save()

        
        # update cash user
        userToUpdate = UserModel.get_by_id(rol.id)
        userToUpdate.efectivo =rol.efectivo - producto.cantidad
        db.session.commit()


        #update product table
        productToUpdate =ProductsModel.get_by_id(producto.id)
        productToUpdate.cantidad = producto.cantidad -1
        db.session.commit()

        
        serialized_compra = compra_schema.dump(compra)
        
        serialized_compra['usuario'] = user_schema.dump(userToUpdate)
        serialized_compra['usuario']['perfil']=""
        serialized_compra['producto'] = product_schema.dump(productToUpdate)
        return ReturnCodes.custom_response(serialized_compra,201,"compra creada")

       
    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))

@compra_api.route("",methods=['GET'])
def get_all():
    try:
   
        
        compras = ComprasModel.get_all()
        serialized_compra = compra_schema.dump(compras,many=True)
        return ReturnCodes.custom_response(serialized_compra,200,"success")

    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))


@compra_api.route("/<int:id>",methods=['GET'])
def get_by_id(id):
    try:
    
        compras = ComprasModel.get_by_id(id)
        if not compras:
            return ReturnCodes.custom_response({},404,"no encontrado")

        serialized_compra = compra_schema.dump(compras)
        return ReturnCodes.custom_response(serialized_compra,200,"success")

    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))

@compra_api.route("/query",methods=["POST"])
def query():
    
    try:
        req_data = request.get_json()
        
        compra_query_schema.load(req_data)

        jsonfiltros = req_data["filtros"]

        compra = ComprasModel.get_by_query(jsonfiltros)
        serialized_compra = compra_schema.dump(compra,many=True)
        return ReturnCodes.custom_response(serialized_compra,200,"ok")
   
    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))



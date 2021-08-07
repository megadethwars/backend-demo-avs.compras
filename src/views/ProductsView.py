from src.utilities import ReturnCodes
from src import utilities
from flask import Flask,request,Response,jsonify,json,Blueprint
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields,schema,validates,Schema
from sqlalchemy import Column

from ..models.UserModel import UserModel,Userschema,UserschemaIn
from ..models.ProductsModel import ProductsModel,Productschema,ProductschemaIn
from ..models.ComprasModel import ComprasModel,Compraschema
from ..utilities import ReturnCodes
from ..DBConnector import DBConnector
import traceback

db=DBConnector.getDB()
product_schema =Productschema()
product_schemaIn = ProductschemaIn()
compras_schema = Compraschema()

product_api = Blueprint("product_api",__name__)

@product_api.route("",methods=["POST"])
def create():
    

    try:
        req_data = request.get_json()
        req_data['perfil']=bytes(json.dumps(req_data['perfil']), 'utf8')
        blob = req_data['perfil']
        data = product_schemaIn.load(req_data)
        rol = ProductsModel.get_by_name(req_data['nombre'])

        if rol:
            return ReturnCodes.custom_response({},409,"el producto ya existe")
        
        if req_data['cantidad']==0:
            return ReturnCodes.custom_response({},409,"la cantidad es cero")

        product = ProductsModel(data,blob)
        product.save()
        serialized_product = dict()
        serialized_product = product_schema.dump(product)
        return ReturnCodes.custom_response(serialized_product,201,"producto creado")

       
    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))



@product_api.route("",methods=['GET'])
def get_all():
    try:
   
        
        products = ProductsModel.get_all()
        serialized_product = product_schema.dump(products,many=True)
        return ReturnCodes.custom_response(serialized_product,200,"success")

    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))


@product_api.route("/<int:id>",methods=['GET'])
def get_by_id(id):
    try:
    
        products = ProductsModel.get_by_id(id)
        if not products:
            return ReturnCodes.custom_response({},404,"no encontrado")

        serialized_product = product_schema.dump(products)
        return ReturnCodes.custom_response(serialized_product,200,"success")

    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))


@product_api.route("/<int:id>",methods=["PUT"])
def update(id):

    try:
        req_data = request.get_json()
        if "perfil" in req_data:
            req_data['perfil']=bytes(json.dumps(req_data['perfil']), 'utf8')
            blob = req_data['perfil']

        data = product_schemaIn.load(req_data,unknown="EXCLUDE")
        products = ProductsModel.get_by_id(id)
        if not products:
            return ReturnCodes.custom_response({},404,"no encontrado")

       
        products.update(data)
        serialized_product = dict()
        serialized_product = product_schema.dump(products)
        return ReturnCodes.custom_response(serialized_product,200,"usuario creado")

       
    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))


@product_api.route("/<int:id>",methods=["DELETE"])
def delete(id):

    try:
        
        #delete compras by producto
        compra =ComprasModel.del_by_producto(id)

        products = ProductsModel.get_by_id(id)
        if not products:
            return ReturnCodes.custom_response({},404,"producto no encontrado o ya fue borrado")
    
        products.delete()
        
        return ReturnCodes.custom_response({"status":"borrado"},200,"producto borrado")

       
    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))
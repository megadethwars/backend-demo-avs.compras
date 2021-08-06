from src.utilities import ReturnCodes
from src import utilities
from flask import Flask,request,Response,jsonify,json,Blueprint
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields,schema,validates,Schema
from sqlalchemy import Column

from ..models.UserModel import UserModel,Userschema,UserschemaIn
from ..models.ProductsModel import ProductsModel,Productschema,ProductschemaIn
from ..utilities import ReturnCodes
from ..DBConnector import DBConnector
import traceback

db=DBConnector.getDB()
product_schema =Productschema()
product_schemaIn = ProductschemaIn()

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
        product = ProductsModel(data,blob)
        product.save()
        serialized_product = dict()
        serialized_product = product_schema.dump(product)
        return ReturnCodes.custom_response(serialized_product,201,"producto creado")

       
    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))
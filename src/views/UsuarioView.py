from src.utilities import ReturnCodes
from src import utilities
from flask import Flask,request,Response,jsonify,json,Blueprint
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields,schema,validates,Schema
from sqlalchemy import Column

from ..models.UserModel import UserModel,Userschema,UserschemaIn
from ..models.ComprasModel import ComprasModel,Compraschema
from ..utilities import ReturnCodes
from ..DBConnector import DBConnector
import traceback

db=DBConnector.getDB()
user_schema =Userschema()
user_schemaIn = UserschemaIn()
compras_schema = Compraschema()


user_api = Blueprint("user_api",__name__)

@user_api.route("",methods=["POST"])
def create():

    try:
        req_data = request.get_json()
        req_data['perfil']=bytes(json.dumps(req_data['perfil']).replace('"',''), 'utf8')
        blob = req_data['perfil']
        data = user_schemaIn.load(req_data)
        rol = UserModel.get_by_name(req_data['username'])

        if rol:
            return ReturnCodes.custom_response({},409,"el usuario ya existe")
        user = UserModel(data,blob)
        user.save()
        serialized_user = dict()
        serialized_user = user_schema.dump(user)
        return ReturnCodes.custom_response(serialized_user,201,"usuario creado")

       
    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))


@user_api.route("",methods=['GET'])
def get_all():
    try:
   
        
        users = UserModel.get_all()
        serialized_user = user_schema.dump(users,many=True)
        return ReturnCodes.custom_response(serialized_user,200,"success")

    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))


@user_api.route("/<int:id>",methods=['GET'])
def get_by_id(id):
    try:
    
        users = UserModel.get_by_id(id)
        if not users:
            return ReturnCodes.custom_response({},404,"no encontrado")

        serialized_user = user_schema.dump(users)
        return ReturnCodes.custom_response(serialized_user,200,"success")

    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))


@user_api.route("/<int:id>",methods=["PUT"])
def update(id):

    try:
        req_data = request.get_json()
        if "perfil" in req_data:
            req_data['perfil']=bytes(json.dumps(req_data['perfil']).replace('"',''), 'utf8')
            blob = req_data['perfil']

        data = user_schemaIn.load(req_data,unknown="EXCLUDE")
        users = UserModel.get_by_id(id)
        if not users:
            return ReturnCodes.custom_response({},404,"no encontrado")

        if req_data['username']:
            repeateduser = UserModel.get_by_name_id(id,req_data['username'])
            if repeateduser:
                return ReturnCodes.custom_response({},404,"usuario repetido")


        users.update(data)
        serialized_user = dict()
        serialized_user = user_schema.dump(users)
        return ReturnCodes.custom_response(serialized_user,200,"usuario creado")

       
    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))


@user_api.route("/<int:id>",methods=["DELETE"])
def delete(id):

    try:
        
        user = UserModel.get_by_id(id)
        if not user:
            return ReturnCodes.custom_response({},404,"usuario no encontrado o ya fue borrado")
        if user.rol ==1:
            serialized_user = user_schema.dump(user)
            serialized_user['perfil']=""
            return ReturnCodes.custom_response(serialized_user,401,"no se debe de borrar el usuario ADMIN")

        #delete compras by producto
        compra =ComprasModel.del_by_producto(id)

        
    
        user.delete()
        
        return ReturnCodes.custom_response({"status":"borrado"},200,"usuario borrado")

       
    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))



@user_api.route("/login",methods=["POST"])
def login():

    try:
        req_data = request.get_json()
        data = user_schemaIn.load(req_data)
        rol = UserModel.get_by_name(req_data['username'])

        if not rol:
            return ReturnCodes.custom_response({},409,"el usuario no existe")

        if rol.password == req_data['password']:
            serialized_user = user_schema.dump(rol)
            return ReturnCodes.custom_response(serialized_user,200,"success")
        else:
            serialized_user = user_schema.dump(rol)
            serialized_user['perfil']=""
            return ReturnCodes.custom_response({},401,"usuario y/o contraseña incorrecto")
        

       
    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))
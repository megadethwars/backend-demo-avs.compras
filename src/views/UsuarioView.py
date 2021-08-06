from src.utilities import ReturnCodes
from src import utilities
from flask import Flask,request,Response,jsonify,json,Blueprint
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields,schema,validates,Schema
from sqlalchemy import Column

from ..models.UserModel import UserModel,Userschema,UserschemaIn
from ..utilities import ReturnCodes
from ..DBConnector import DBConnector
import traceback

db=DBConnector.getDB()
user_schema =Userschema()
user_schemaIn = UserschemaIn()

user_api = Blueprint("user_api",__name__)

@user_api.route("",methods=["POST"])
def create():

    try:
        req_data = request.get_json()
        req_data['perfil']=bytes(json.dumps(req_data['perfil']), 'utf8')
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
        return ReturnCodes.custom_response(serialized_user,201,"success")

    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))


@user_api.route("/<int:id>",methods=['GET'])
def get_by_id(id):
    try:
    
        users = UserModel.get_by_id(id)
        if not users:
            return ReturnCodes.custom_response({},404,"no encontrado")

        serialized_user = user_schema.dump(users)
        return ReturnCodes.custom_response(serialized_user,201,"success")

    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))


@user_api.route("/<int:id>",methods=["PUT"])
def update(id):

    try:
        req_data = request.get_json()
        if "perfil" in req_data:
            req_data['perfil']=bytes(json.dumps(req_data['perfil']), 'utf8')
            blob = req_data['perfil']

        data = user_schemaIn.load(req_data,unknown="EXCLUDE")
        user = users = UserModel.get_by_id(id)
        if not user:
            return ReturnCodes.custom_response({},404,"no encontrado")

       
        users.update(data)
        serialized_user = dict()
        serialized_user = user_schema.dump(users)
        return ReturnCodes.custom_response(serialized_user,201,"usuario creado")

       
    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))
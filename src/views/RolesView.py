from src.utilities import ReturnCodes
from src import utilities
from flask import Flask,request,Response,jsonify,json,Blueprint
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields,schema,validates,Schema
from sqlalchemy import Column
from ..models.RolesModel import RoleModel,Roleschema,RoleschemaIn
from ..utilities import ReturnCodes
from ..DBConnector import DBConnector
import traceback

db=DBConnector.getDB()
role_schema =Roleschema()
roleschemaIn = RoleschemaIn()

role_api = Blueprint("role_api",__name__)

@role_api.route("",methods=["POST"])
def create():
    

    try:
        req_data = request.get_json()
        data = roleschemaIn.load(req_data)
        rol = RoleModel.get_by_name(req_data['cargo'])

        if rol:
            return ReturnCodes.custom_response({},409,"el cargo y existe")
        role = RoleModel(data)
        role.save()
        serialized_role = dict()
        serialized_role = role_schema.dump(role)
        return ReturnCodes.custom_response(serialized_role,201,"Rol creado")

       
    except Exception as ex:
        return ReturnCodes.custom_response({},409,str(ex))
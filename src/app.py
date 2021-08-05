from flask import Flask,request,Response,jsonify,json
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields,schema,validates,Schema
from sqlalchemy import Column
from .utilities import ReturnCodes
#from .views.RolesView import role_api as role_blueprint
from .DBConnector import DBConnector


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:neology@localhost:3306/db_avs'

    DBConnector.InitConnection(app)

    db=DBConnector.getDB()


    from .views.RolesView import role_api as role_blueprint
    from .views.UsuarioView import user_api as usuario_blueprint

    app.register_blueprint(role_blueprint,url_prefix="/api/roles")
    app.register_blueprint(usuario_blueprint,url_prefix="/api/usuarios")

    class Task(db.Model):

        __tablename__ ="Tasks"

        id = db.Column(db.Integer,primary_key=True)
        title = db.Column(db.String(70))
        otro = db.Column(db.String(70))
        otromas = db.Column(db.String(70))
        def __init__(self,title):
            self.title=title



    db.create_all()

    class TaskSchema(Schema):
        id = fields.Int()
        title=fields.String()
        

    taskschema = TaskSchema()

    @app.route('/')
    def home():
        return "OK"

    @app.route('/insert',methods=['POST'])
    def insert():
        print(request.json)
        task =Task(request.json['title'])
        db.session.add(task)
        db.session.commit()

        tsk = taskschema.dump(task)
        return tsk
    

    return app


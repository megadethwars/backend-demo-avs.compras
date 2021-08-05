from flask import Response,json

def custom_response(res,statuscode,message):

    response ={
        "data":res,
        "message":message
    }

    return Response(mimetype="application/json",response=json.dumps(response),status=statuscode)
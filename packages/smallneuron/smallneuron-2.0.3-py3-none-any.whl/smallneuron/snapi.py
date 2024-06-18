#!/usr/bin/python3
from flask import Flask, request,  make_response
from flask_restful import Resource, Api,  reqparse
from requests import get, put, post
import threading
import syslog
from time import sleep
import sys,  json
from .logger import Logger
log= Logger("smallneuron.SnHttp")

#

class HttpEvent (Resource):
    def get(self,  action, kart_id=None):
        log.debug( request.remote_addr," Planner status",  action)
        log.debug( "Planner ",  action)
        
        # Over all status
        if (action=="status"):
            return {"response":  "OK", 
            "status":str("Im Happy") ,  
            "response": "OK",
            "task_id": 0,
            "task_type": "status",
            "name": socket.gethostname(),
            "type": "planner", 
            "karts":getKartList(),  
            "layout":planner.getLayout() }  ,  200  # 200 (OK)         
          
        # Current plan status in .dot format
        elif (action == "plan"):
            semAcquire()
            response = make_response(str(planner.getDotPlan()),  200)
            semRelease()
            response.mimetype = "text/plain"
            return response
        # Retorna las posiciones ajustadas al offset del kart
        elif (action == "positions"):
            k = getKart(kart_id)
            if k == None:
                logger(syslog.LOG_ERR,  request.remote_addr," kart positions:",   str(kart_id) ,  " not found")
                return { "response":"FAIL", "msg":  str(kart_id) + " not found"} ,  404 # 404 (Not Found)
            else:
                return k.getPositions()
        elif (action == "transfers"):
            k = getKart(kart_id)
            if k == None:
                logger(syslog.LOG_ERR,  request.remote_addr," kart transfers:",   str(kart_id) ,  " not found")
                return { "response":"FAIL", "msg":  str(kart_id) + " not found"} ,  404 # 404 (Not Found)
            else:
                return planner.kartTransfers[kart_id]
        elif (action == "outOfService"):
            planner.setOutOfService(True)
            return { "response":"OK", "msg":  action} ,  200 # 200 OK
        elif (action == "onService"):
            planner.setOutOfService(False)
            return { "response":"OK", "msg":  action} ,  200 # 200 OK
        else:
            return None ,  405 # 405 (Method Not Allowed)
            
    def post(self, action=None):
        
        parser = reqparse.RequestParser()
        parser.add_argument('task_type',required=False, default="")
        parser.add_argument('url',required=False, default="")
        parser.add_argument('post', required=False, default="{}")
        args = parser.parse_args()
        logger(syslog.LOG_INFO,  request.remote_addr," Request:",  args)
        print("PlannerServer POST end parse", args)
        
        if action == None and args["task_type"] == "status":
            print("PlannerServer status")
            return {
            "response": "OK",
            "tdropask_id": 0,
            "task_type": "status",
            "name": socket.gethostname(),
            "type": "planner"
            }, 200
        elif action == "forward":
            content = request.get_json(silent=True)    # Reenviamos el post y retornamos lo recibido
            print("forwarding content ", content )
            logger(syslog.LOG_INFO,  "forwarding to ", content["url"], " payload ", content["post"] )
            r=post(args["url"], json=content["post"]);
            return r.json(), r.status_code
        else:
            return None, 405
            
api.add_resource(PlannerServer, '/<string:action>','/<string:action>/<string:kart_id>')  # Kart list status, and plan
api.add_resource(Order, '/order', '/order/<int:order_id>')                        # POST New order, GET Order status ,DELETE Order    ,  '/order/<int:order_id>',  endpoint="order_id"
api.add_resource(Task, '/task/<int:task_id>')  # End task
api.add_resource(Kart, '/kart/<string:kart_id>', '/kart/<string:component>/<string:code>')   # Checkin and send event

class SnHttp(Flask):
    def __init__(self):
        super().__init__(__name__)
        self.app = Flask(__name__)
        self.api = Api(self.app)
    
    def add_resource(self, resource, *urls, **kwargs):
        self.api.add_resource(resource, urls, kwargs)

    def start(self, service_port=9000):
        self.app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024
        self.app.run(debug=False, host= '0.0.0.0', port=service_port)


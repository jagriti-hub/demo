from aws_xray_sdk.core import xray_recorder, patch_all
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from aws_xray_sdk.ext.flask_sqlalchemy.query import XRayFlaskSqlAlchemy
import requests
from flask import Flask, jsonify
from flask import request
import re
import sys,os,boto3
for dbfiles in os.listdir("/{{apiname}}/dbconf/"):
    exec(open("/{{apiname}}/dbconf/" + dbfiles).read())
app = Flask(__name__)
xray_recorder.configure(service='My Flask Web Application')
XRayMiddleware(app, xray_recorder)
patch_all()
for apifiles in os.listdir("/{{apiname}}/apiactions/"):
    exec(open("/{{apiname}}/apiactions/" + apifiles).read())
if __name__ == "__main__":
    app.run()
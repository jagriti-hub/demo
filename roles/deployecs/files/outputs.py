import json,datetime,boto3, sys, os, time
from botocore.exceptions import ClientError
from boto3 import session
from botocore.config import Config
import decimal
import yaml
import io
import pathlib
import shutil

DeployEnvTableName = sys.argv[1]
DeployId  =  sys.argv[2]
# DeployEnvTableName = "DeployEnvironment"
# DeployId  =  "ekshelm"

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb=boto3.resource("dynamodb",region_name='us-east-1')
envdb=dynamodb.Table(DeployEnvTableName)
Environment = envdb.get_item(Key={'DeployId': DeployId})['Item']
Environment = json.loads(json.dumps(Environment, cls=DecimalEncoder))
Outputs = Environment['Outputs'][0]
json_object = json.dumps(Outputs, indent = 2) 
x = sys.argv[3]
with open(x,'w') as f:
    f.write(json_object) 





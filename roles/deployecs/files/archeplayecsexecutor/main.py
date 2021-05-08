import json,boto3,sys,os,botocore
from boto3 import session
from botocore.config import Config
from botocore.exceptions import ClientError

import datetime,time,decimal
import yaml,io

import logging
logging.basicConfig()
logger = logging.getLogger()
import aws_lambda_logging


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

EnvTableName = os.environ['EnvironmentDb']
DeployId  =  os.environ['DeployId']
Action = os.environ['Action']
AssumeRoleName=os.environ['AssumeRoleName']

# EnvTableName = "DeployTable"
# DeployId  =  "EKSCTL-testcase1"
# # Action = "Delete"
# AssumeRoleName= "cloud9_admin"

def get_acc_permission(AccountId,Region,SessionName):
    sts = boto3.client('sts')
    keys = sts.assume_role(RoleArn="arn:aws:iam::{0}:role/{1}".format(AccountId,AssumeRoleName),RoleSessionName=SessionName)['Credentials']
    os.environ['AWS_ACCESS_KEY_ID']=keys['AccessKeyId']
    os.environ['AWS_SECRET_ACCESS_KEY']=keys['SecretAccessKey']
    os.environ['AWS_SESSION_TOKEN']=keys['SessionToken']
    os.environ['AWS_DEFAULT_REGION']=Region
    connection = boto3.session.Session(aws_access_key_id=keys['AccessKeyId'],
                            aws_secret_access_key=keys['SecretAccessKey'],
                            aws_session_token=keys['SessionToken'],
                            region_name=Region)
    return connection
  
def update_deployedenvdb(db,deployid,key,value):
    db.update_item(
                    Key={"DeployId":deployid},
                    UpdateExpression = 'SET #k=:value',
                    ExpressionAttributeNames={'#k': key},
                    ExpressionAttributeValues = {':value':value}
                    ) 

aws_lambda_logging.setup(level='INFO',DeployId=DeployId,Action=Action)

dynamodb=boto3.resource("dynamodb",region_name='us-east-1')
envdb=dynamodb.Table(EnvTableName)

Environment = envdb.get_item(Key={'DeployId': DeployId})['Item']

Environment = json.loads(json.dumps(Environment, cls=DecimalEncoder))

Input=Environment['Parameters']
# for k,v in Environment['Parameters'].items():
#     Input[k]=v['value']
ipopen = open(os.path.join(os.path.dirname(__file__),"input.json"), "w")
json.dump(Input,ipopen,indent=4)
ipopen.close()
    

Template=Environment['Template']
Template = yaml.safe_load(Template)
codeopen = open(os.path.join(os.path.dirname(__file__),"code.yaml"), "w")
yaml.dump(Template, codeopen, default_flow_style=False, allow_unicode=False)
# with open (os.path.join(os.path.dirname(__file__),'code.yaml'),'r+') as f:
#     Template = yaml.load(f)

if "Outputs" in Environment:
	Ouput={"Output":Environment['Outputs']}
else:
	Ouput={"Output":[]}

opopen = open(os.path.join(os.path.dirname(__file__),"output.json"), "w")
json.dump(Ouput,opopen,indent=4)
opopen.close()

for resource in Template['Resources']:
    temp = Template['Resources'][resource]['Code']
    with open(os.path.join(os.path.dirname(__file__),Template['Resources'][resource]['Type']),'w') as f:
        f.write(temp)
AccountId=Environment['AccountId']
if Action == "Create":
    connection=get_acc_permission(Environment['AccountId'],Environment['Region'],Environment['EmailId'])
    code=Template['Resources']['Create']['Code']
    print(code)
    try:
        exec(code)
        
        update_deployedenvdb(envdb,DeployId,'State',"Running")
        with open (os.path.join(os.path.dirname(__file__),'output.json'),'r+') as f:
            out = json.load(f)    
        update_deployedenvdb(envdb,DeployId,'Outputs',out['Output'])
    except Exception as e:
        update_deployedenvdb(envdb,DeployId,'State',"Failed")
        print(e)
        
elif Action == "Delete":
    connection=get_acc_permission(Environment['AccountId'],Environment['Region'],Environment['EmailId'])
    code=Template['Resources']['Delete']['Code']
    print(code)
    try:
        exec(code)
        update_deployedenvdb(envdb,DeployId,'State',"Deleted")
        update_deployedenvdb(envdb,DeployId,'Outputs',{})
    except:
        update_deployedenvdb(envdb,DeployId,'State',"Failed")
   
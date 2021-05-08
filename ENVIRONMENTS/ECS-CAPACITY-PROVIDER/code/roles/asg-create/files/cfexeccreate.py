import json,boto3,sys,os
from botocore.exceptions import ClientError

import decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

Region = sys.argv[1]
Parameterfile = sys.argv[2]
StackName = sys.argv[3]
Template = sys.argv[4]
BucketName = sys.argv[5]
Deploymentid = sys.argv[6]
envdeploymentfolder = sys.argv[7]
s3_client = boto3.client('s3')
s3 = boto3.resource('s3')
cf = boto3.client('cloudformation',region_name=Region)
# s3_client.download_file(BucketName, "/events"+"/"+Deploymentid+"/event.json",'/tmp/event.json')
# event=json.loads(open(r'/tmp/event.json').read())
# s3_client.download_file(BucketName, "/events"+"/"+Deploymentid+"/output.json",'/tmp/out.json')
# outpt=json.loads(open(r'/tmp/out.json').read())
event={}
outpt={}
params=[]

file = open(Parameterfile, 'r')
Parameterss = file.read()

tempfile = open(Template, 'r')
Template = tempfile.read()

Parameters = json.loads(Parameterss) 


for k,v in Parameters.items():
    p={'ParameterKey': k,'ParameterValue': v}
    params.append(p)
# print("params:", params)
cf_response=cf.create_stack(
                StackName=StackName,
                TemplateBody=Template,
                Parameters=params,
                Capabilities=['CAPABILITY_IAM','CAPABILITY_NAMED_IAM','CAPABILITY_AUTO_EXPAND']
                )
outpt['State']='Provisioning'

stackid = cf_response['StackId']
print(stackid)

# try:
#     stack=cf.describe_stacks(StackName=StackName)['Stacks'][0]
#     outpt['State']=stack['StackStatus']
#     res_events=cf.describe_stack_events(StackName=StackName)
#     stk_events=res_events['StackEvents']
#     while "NextToken" in res_events:
#         res_events=cf.describe_stack_events(StackName=StackName,NextToken=res_events['NextToken'])
#         stk_events=stk_events+res_events['StackEvents']
#     event['StepEvents']=json.loads(json.dumps(stk_events,default=str))
#     if 'Outputs' in stack:
#         outpt['Outputs']=stack['Outputs']
# except ClientError as e:
#     if 'does not exist' in str(e):
#         outpt['State']='NotPresent'
#     else:
#         outpt['State']='Failed'

# Outputs = json.dumps(outpt)
# print(Outputs)

# file = open(envdeploymentfolder+"/output.json", 'w+')
# file.close()

# with open(envdeploymentfolder+"/output.json","r+") as f:
#     data = json.load(f)
#     data.update(Outputs)
#     json.dump(data, f, indent=4)

# s3.Object(BucketName,"/outputs"+"/"+Deploymentid+"/output.json").put(Body=json.dumps(outpt))
# s3.Object(BucketName,"/events"+"/"+Deploymentid+"/event.json").put(Body=json.dumps(event))

   
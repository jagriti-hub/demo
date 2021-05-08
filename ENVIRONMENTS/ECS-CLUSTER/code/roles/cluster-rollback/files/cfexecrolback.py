import json,boto3,sys,os,time
from botocore.exceptions import ClientError
Region = sys.argv[1]
Parameterss = sys.argv[2]
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

# stack=cf.describe_stacks(StackName=StackName)['Stacks'][0]
# stack_status = stack['StackStatus']
# stackid = stack['StackId']

try:
    stack=cf.describe_stacks(StackName=StackName)['Stacks'][0]
    stack_status = stack['StackStatus']
    outpt['State']=stack['StackStatus']
    delete_stack_fnc = cf.delete_stack( StackName=StackName )
except ClientError as e:
    if 'does not exist' in str(e):
        outpt['State']='NotPresent'
    else:
        outpt['State']='Failed'

Outputs = outpt
print(Outputs)
# print("Outputs type:", type(Outputs))
# print("Outputs:",Outputs)
# print("Outputs type:", type(Outputs))


# try:
#     data = json.loads(open(envdeploymentfolder+"/ecsoutput.json").read())
# except:
#     data = {}
#     data.update(Outputs)
#     config_f = open(envdeploymentfolder+"/ecsoutput.json", "a+")
#     config_f.write(json.dumps(Outputs, indent=4))
#     config_f.close()




# s3.Object(BucketName,"/outputs"+"/"+Deploymentid+"/output.json").put(Body=json.dumps(outpt))
# s3.Object(BucketName,"/events"+"/"+Deploymentid+"/event.json").put(Body=json.dumps(event))

   
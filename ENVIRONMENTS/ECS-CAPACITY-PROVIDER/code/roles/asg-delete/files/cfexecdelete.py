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
event={}
outpt={}
params=[]

try:
    stack=cf.describe_stacks(StackName=StackName)['Stacks'][0]
    stack_status = stack['StackStatus']
    outpt['State']=stack['StackStatus']
    delete_stack_fnc = cf.delete_stack( StackName=StackName )
    del_stack_status = stack['StackStatus']
    
except ClientError as e:
    if 'does not exist' in str(e):
        outpt['State']='NotPresent'
    else:
        outpt['State']='Failed'

Outputs = outpt
print(Outputs)
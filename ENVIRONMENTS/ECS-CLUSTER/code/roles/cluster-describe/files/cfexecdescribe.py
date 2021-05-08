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
stack=cf.describe_stacks(StackName=StackName)['Stacks'][0]
stack_status = stack['StackStatus']
while stack_status not in [ "CREATE_COMPLETE", "CREATE_FAILED", "ROLLBACK_IN_PROGRESS", "ROLLBACK_FAILED", "ROLLBACK_COMPLETE", "DELETE_IN_PROGRESS", "DELETE_FAILED", "DELETE_COMPLETE" ]:
    time.sleep(30)
    try:
        stack=cf.describe_stacks(StackName=StackName)['Stacks'][0]
        stack_status = stack['StackStatus']
        outpt['State']=stack['StackStatus']
        res_events=cf.describe_stack_events(StackName=StackName)
        stk_events=res_events['StackEvents']
        while "NextToken" in res_events:
            res_events=cf.describe_stack_events(StackName=StackName,NextToken=res_events['NextToken'])
            stk_events=stk_events+res_events['StackEvents']
        event['StepEvents']=json.loads(json.dumps(stk_events,default=str))
        if 'Outputs' in stack:
            outpt['Outputs']=stack['Outputs']
    except ClientError as e:
        if 'does not exist' in str(e):
            stack_status = 'DELETE_COMPLETE'
            outpt['State']='NotPresent'
        else:
            outpt['State']='Failed'

Outputs = outpt
print(Outputs)
# print("Outputs type:", type(Outputs))
# print("Outputs:",Outputs)
# print("Outputs type:", type(Outputs))


try:
    data = json.loads(open(envdeploymentfolder+"/ecsoutput.json").read())
except:
    data = {}
data.update(Outputs)
config_f = open(envdeploymentfolder+"/ecsoutput.json", "a+")
config_f.write(json.dumps(Outputs, indent=4))
config_f.close()




# s3.Object(BucketName,"/outputs"+"/"+Deploymentid+"/output.json").put(Body=json.dumps(outpt))
# s3.Object(BucketName,"/events"+"/"+Deploymentid+"/event.json").put(Body=json.dumps(event))

   
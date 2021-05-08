import json,boto3,sys,os,time
from botocore.exceptions import ClientError
Region = sys.argv[1]
StackName = sys.argv[2]
envdeploymentfolder = sys.argv[3]
cf = boto3.client('cloudformation',region_name=Region)
time.sleep(60)
event={}
outpt={}
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
            Events = event
            try:
                eventdata = json.loads(open(envdeploymentfolder+"/eksctlevent.json").read())
            except:
                eventdata = {}
            eventdata.update(Events)
            config_f = open(envdeploymentfolder+"/eksctlevent.json", "a+")
            config_f.write(json.dumps(eventdata, indent=4))
            config_f.close()
        if 'Outputs' in stack:
            outpt['Outputs']=stack['Outputs']
    except ClientError as e:
        if 'does not exist' in str(e):
            outpt['State']='NotPresent'
        else:
            outpt['State']='Failed'

Outputs = outpt
print(Outputs)

try:
    data = json.loads(open(envdeploymentfolder+"/eksoutput.json").read())
except:
    data = {}
data.update(Outputs)
config_f = open(envdeploymentfolder+"/eksoutput.json", "a+")
config_f.write(json.dumps(data, indent=4))
config_f.close()
time.sleep(700)
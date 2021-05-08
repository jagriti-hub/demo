import sys,os,boto3,time,math,random
import logging,json

path=sys.argv[1]
datapath=sys.argv[2]

def create_input(tableconf):
    tableindexes = tableconf["indexes"]
    paramstructure={}
    paramstructure["TableName"]=tableconf["tablename"]
    AttributeDefinitions=[]
    for attschema in tableconf["schema"]:
        AttributeDefinition = {
            "AttributeName": attschema["attributename"],
            "AttributeType": attschema["attributetype"]
        }
        AttributeDefinitions.append(AttributeDefinition)
    paramstructure["AttributeDefinitions"]=AttributeDefinitions
    primarykeyschema = []
    primarykey = {
        "AttributeName": tableindexes["primary"]["key"],
        "KeyType": "HASH"
    }
    primarykeyschema.append(primarykey)
    if "sortkey" in tableindexes["primary"] and tableindexes["primary"]['sortkey']!="":
        sortkey = {
            "AttributeName": tableindexes["primary"]["sortkey"],
            "KeyType": "RANGE"
        }
        primarykeyschema.append(sortkey)
    paramstructure["KeySchema"]=primarykeyschema
    if tableindexes["primary"]["infra"]["ondemand"] == True:
        paramstructure["BillingMode"]="PAY_PER_REQUEST"
        paramstructure["ProvisionedThroughput"]={
            "ReadCapacityUnits": 0,
            "WriteCapacityUnits": 0
        }
    elif tableindexes["primary"]["infra"]["ondemand"] == False:
        paramstructure["BillingMode"]="PROVISIONED"
        paramstructure["ProvisionedThroughput"]={
            "ReadCapacityUnits": tableindexes["primary"]["infra"]["iops"]["read"],
            "WriteCapacityUnits": tableindexes["primary"]["infra"]["iops"]["write"]
        }
    GlobalSecInd=[]
    if "secondary" in tableindexes:
        secondkeyschema = {}
        keyschema = []
        for secondarykey in tableindexes["secondary"]:
            if "key" in secondarykey:
                secondkey = {
                    "AttributeName": secondarykey["key"],
                    "KeyType": "HASH"
                }
                keyschema.append(secondkey)
            if "sortkey" in  secondarykey and secondarykey["sortkey"] != "":
                secondsortkey = {
                    "AttributeName": secondarykey["sortkey"],
                    "KeyType": "RANGE"
                }
                keyschema.append(secondsortkey)
            secondkeyschema["KeySchema"]=keyschema
            secondkeyschema["IndexName"]=secondarykey["indexname"]
            if secondarykey["infra"]["ondemand"] == True and tableindexes["primary"]["infra"]["ondemand"] == True:
                secondkeyschema["ProvisionedThroughput"]={
                    "ReadCapacityUnits": 0,
                    "WriteCapacityUnits": 0
                }
            elif secondarykey["infra"]["ondemand"] == False and tableindexes["primary"]["infra"]["ondemand"] == True:
                secondkeyschema["ProvisionedThroughput"]={
                    "ReadCapacityUnits": 0,
                    "WriteCapacityUnits": 0
                }
            elif secondarykey["infra"]["ondemand"] == False and tableindexes["primary"]["infra"]["ondemand"] == False:
                secondkeyschema["ProvisionedThroughput"]={
                    "ReadCapacityUnits": secondarykey["infra"]["iops"]["read"],
                    "WriteCapacityUnits": secondarykey["infra"]["iops"]["write"]
                }
            elif secondarykey["infra"]["ondemand"] == True and tableindexes["primary"]["infra"]["ondemand"] == False:
                secondkeyschema["ProvisionedThroughput"]={
                    "ReadCapacityUnits": tableindexes["primary"]["infra"]["iops"]["read"],
                    "WriteCapacityUnits": tableindexes["primary"]["infra"]["iops"]["write"]
                    }
            secondkeyschema["Projection"]={
                "ProjectionType": "ALL"
                }
            GlobalSecInd.append(secondkeyschema)
        paramstructure["GlobalSecondaryIndexes"]=GlobalSecInd
    return(paramstructure)

def createcf():
    if os.path.exists(datapath):
        file_object=open(datapath,"r")
        datastring=file_object.read()
        data=json.loads(datastring)
    TableProperties=[]
    for tableconf in data:
        TableProperty=create_input(tableconf)
        TableProperties.append(TableProperty)
    print(TableProperties)
    ModuleTemplate={
                    "AWSTemplateFormatVersion": "2010-09-09",
                    "Resources": {},
                    "Outputs": {}
                }
    for prop in TableProperties:
        ModuleTemplate["Resources"].update({
            prop["TableName"]: {
                "Type": "AWS::DynamoDB::Table",
                "Properties": prop
            }
        })
        ModuleTemplate["Outputs"].update({
            prop["TableName"]+"output": {
                "Description": "Dynamodb TableName",
                "Value": {"Ref": prop["TableName"]}
                   
            }
        })

    modulepath=path+"/tablecf.json"
    f=open(modulepath,"w+")
    directory = os.path.dirname(modulepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    datastring=json.dumps(ModuleTemplate)
    data_folder=open(modulepath, "w")
    data_folder.write(datastring)

createcf()
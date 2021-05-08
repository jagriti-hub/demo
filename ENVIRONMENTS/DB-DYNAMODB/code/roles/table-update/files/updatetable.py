import boto3,json,time,decimal,ast
import sys,os
table1 = sys.argv[1]
Region = sys.argv[2]
secondarykey1 = sys.argv[3]
dynamodb = boto3.client('dynamodb',region_name=Region)
table=ast.literal_eval(table1)
secondarykey = ast.literal_eval(secondarykey1)
indexnames=[]
try:
    response1 = dynamodb.describe_table(TableName=table['tablename'])['Table']['GlobalSecondaryIndexes']
    for item in response1:
        indexnames.append(item['IndexName'])
except Exception as e:
    print(e)
    
try:
    if secondarykey['secondarykey'] != "":
        try:
            if secondarykey['action'] == "Create":
                if secondarykey['secondarykey'] not in indexnames:
                    if secondarykey['infra']['readiops'] == 0 and secondarykey['infra']['writeiops'] == 0:
                        if secondarykey['secondarysortkey'] == "":
                            response = dynamodb.update_table(
                                AttributeDefinitions=[
                                    {
                                        'AttributeName': table['primarykey'],
                                        'AttributeType': table['primarykeyatt']
                                    },
                                    {
                                        'AttributeName': secondarykey['secondarykey'],
                                        'AttributeType': secondarykey['secondarykeyatt']
                                    },
                                ],
                                TableName=table['tablename'],
                                GlobalSecondaryIndexUpdates=[
                                    {
                                        'Create': {
                                            'IndexName': secondarykey['secondarykey'],
                                            'KeySchema': [
                                                {
                                                    'AttributeName': secondarykey['secondarykey'],
                                                    'KeyType': 'HASH'
                                                },
                                            ],
                                            'Projection': {
                                                'ProjectionType': 'ALL',
                                            }
                                        },
                                    },
                                ],
                            )
                            indexres = dynamodb.describe_table(TableName=table['tablename'])['Table']['GlobalSecondaryIndexes']
                            count=0
                            for state in indexres:
                                if state['IndexStatus'] == 'CREATING':
                                    counter=count
                                    status = state['IndexStatus']
                                    while status != 'ACTIVE':
                                        print(status)
                                        time.sleep(10)
                                        response1 = dynamodb.describe_table(TableName=table['tablename'])['Table']['GlobalSecondaryIndexes']
                                        status = response1[counter]['IndexStatus']
                                count = count+1
                        elif secondarysortkey['secondarysortkey'] != "":
                            response = dynamodb.update_table(
                                AttributeDefinitions=[
                                    {
                                        'AttributeName': table['primarykey'],
                                        'AttributeType': table['primarykeyatt']
                                    },
                                    {
                                        'AttributeName': secondarykey['secondarykey'],
                                        'AttributeType': secondarykey['secondarykeyatt']
                                    },
                                    {
                                        'AttributeName': secondarykey['secondarysortkey'],
                                        'AttributeType': secondarykey['secondarysortkeyatt']
                                    }
                                ],
                                TableName=table['tablename'],
                                GlobalSecondaryIndexUpdates=[
                                    {
                                        'Create': {
                                            'IndexName': secondarykey['secondarykey'],
                                            'KeySchema': [
                                                {
                                                    'AttributeName': secondarykey['secondarykey'],
                                                    'KeyType': 'HASH'
                                                },
                                                {
                                                    'AttributeName': secondarykey['secondarysortkey'],
                                                    'KeyType': 'RANGE'
                                                }
                                            ],
                                            'Projection': {
                                                'ProjectionType': 'ALL',
                                            }
                                        },
                                    },
                                ],
                            )
                            indexres = dynamodb.describe_table(TableName=table['tablename'])['Table']['GlobalSecondaryIndexes']
                            count=0
                            for state in indexres:
                                if state['IndexStatus'] == 'CREATING':
                                    counter=count
                                    status = state['IndexStatus']
                                    while status != 'ACTIVE':
                                        print(status)
                                        time.sleep(10)
                                        response1 = dynamodb.describe_table(TableName=table['tablename'])['Table']['GlobalSecondaryIndexes']
                                        status = response1[counter]['IndexStatus']
                                count = count+1
                    elif secondarykey['infra']['readiops'] != 0 and secondarykey['infra']['writeiops'] != 0:
                        if secondarykey['secondarysortkey'] == "":
                            response = dynamodb.update_table(
                                AttributeDefinitions=[
                                    {
                                        'AttributeName': table['primarykey'],
                                        'AttributeType': table['primarykeyatt']
                                    },
                                    {
                                        'AttributeName': secondarykey['secondarykey'],
                                        'AttributeType': secondarykey['secondarykeyatt']
                                    },
                                ],
                                TableName=table['tablename'],
                                GlobalSecondaryIndexUpdates=[
                                    {
                                        'Create': {
                                            'IndexName': secondarykey['secondarykey'],
                                            'KeySchema': [
                                                {
                                                    'AttributeName': secondarykey['secondarykey'],
                                                    'KeyType': 'HASH'
                                                },
                                            ],
                                            'Projection': {
                                                'ProjectionType': 'ALL',
                                            },
                                            'ProvisionedThroughput': {
                                                'ReadCapacityUnits': secondarykey['infra']['readiops'],
                                                'WriteCapacityUnits': secondarykey['infra']['writeiops']
                                            }
                                        },
                                    },
                                ],
                            )
                            indexres = dynamodb.describe_table(TableName=table['tablename'])['Table']['GlobalSecondaryIndexes']
                            count=0
                            for state in indexres:
                                if state['IndexStatus'] == 'CREATING':
                                    counter=count
                                    status = state['IndexStatus']
                                    while status != 'ACTIVE':
                                        print(status)
                                        time.sleep(10)
                                        response1 = dynamodb.describe_table(TableName=table['tablename'])['Table']['GlobalSecondaryIndexes']
                                        status = response1[counter]['IndexStatus']
                                count = count+1
                        elif secondarykey['secondarysortkey'] != "":
                            response = dynamodb.update_table(
                                AttributeDefinitions=[
                                    {
                                        'AttributeName': table['primarykey'],
                                        'AttributeType': table['primarykeyatt']
                                    },
                                    {
                                        'AttributeName': secondarykey['secondarykey'],
                                        'AttributeType': secondarykey['secondarykeyatt']
                                    },
                                    {
                                        'AttributeName': secondarykey['secondarysortkey'],
                                        'AttributeType': secondarykey['secondarysortkeyatt']
                                    }
                                ],
                                TableName=table['tablename'],
                                GlobalSecondaryIndexUpdates=[
                                    {
                                        'Create': {
                                            'IndexName': secondarykey['secondarykey'],
                                            'KeySchema': [
                                                {
                                                    'AttributeName': secondarykey['secondarykey'],
                                                    'KeyType': 'HASH'
                                                },
                                                {
                                                    'AttributeName': secondarykey['secondarysortkey'],
                                                    'KeyType': 'RANGE'
                                                }
                                            ],
                                            'Projection': {
                                                'ProjectionType': 'ALL',
                                            },
                                            'ProvisionedThroughput': {
                                                'ReadCapacityUnits': secondarykey['infra']['readiops'],
                                                'WriteCapacityUnits': secondarykey['infra']['writeiops']
                                            }
                                        },
                                    },
                                ],
                            )
                            indexres = dynamodb.describe_table(TableName=table['tablename'])['Table']['GlobalSecondaryIndexes']
                            count=0
                            for state in indexres:
                                if state['IndexStatus'] == 'CREATING':
                                    counter=count
                                    status = state['IndexStatus']
                                    while status != 'ACTIVE':
                                        print(status)
                                        time.sleep(10)
                                        response1 = dynamodb.describe_table(TableName=table['tablename'])['Table']['GlobalSecondaryIndexes']
                                        status = response1[counter]['IndexStatus']
                                count = count+1
                elif secondarykey['secondarykey'] in indexnames:
                    print('secondarykey already present')
                    
            if secondarykey['action'] == "Delete":
                if secondarykey['secondarykey'] in indexnames: 
                    response = dynamodb.update_table(TableName=table['tablename'], GlobalSecondaryIndexUpdates=[{'Delete': {'IndexName': secondarykey['secondarykey']}}])
                    status = dynamodb.describe_table(TableName=table['tablename'])['Table']['TableStatus']
                    while status in ['UPDATING','DELETING','CREATING']:
                        time.sleep(10)
                        status = dynamodb.describe_table(TableName=table['tablename'])['Table']['TableStatus']
                else:
                    print('secondarykey not present')
        except Exception as e:
            print(e)
except Exception as e:
    sys.exit(e)
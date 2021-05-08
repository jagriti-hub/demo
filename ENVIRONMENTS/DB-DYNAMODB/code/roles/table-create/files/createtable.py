import boto3,json,time,decimal,ast
import sys,os
table1 = sys.argv[1]
Region = sys.argv[2]
dynamodb = boto3.client('dynamodb',region_name=Region)
table=ast.literal_eval(table1)

tables = dynamodb.list_tables()
tablenames = tables['TableNames']
if table['tablename'] not in tablenames:
    if table['infra']['readiops'] == 0 and table['infra']['writeiops'] == 0:
        if table['sortkey']=="":
            response = dynamodb.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': table['primarykey'],
                        'AttributeType': table['primarykeyatt']
                    }
                ],
                TableName=table['tablename'],
                KeySchema=[
                    {
                        'AttributeName': table['primarykey'],
                        'KeyType': 'HASH'
                    }
                ],
                BillingMode='PAY_PER_REQUEST'
            )
        elif table['sortkey']!="":
            response = dynamodb.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': table['primarykey'],
                        'AttributeType': table['primarykeyatt']
                    },
                    {
                        'AttributeName': table['sortkey'],
                        'AttributeType': table['sortkeyatt']
                    }
                ],
                TableName=table['tablename'],
                KeySchema=[
                    {
                        'AttributeName': table['primarykey'],
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': table['sortkey'],
                        'KeyType': 'RANGE'
                    }
                ],
                BillingMode='PAY_PER_REQUEST'
            )
        
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=table['tablename'])
        
    elif table['infra']['readiops'] != 0 and table['infra']['writeiops'] != 0:
        if table['sortkey']=="":
            response = dynamodb.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': table['primarykey'],
                        'AttributeType': table['primarykeyatt']
                    }
                ],
                TableName=table['tablename'],
                KeySchema=[
                    {
                        'AttributeName': table['primarykey'],
                        'KeyType': 'HASH'
                    }
                ],
                BillingMode='PROVISIONED',
                ProvisionedThroughput={
                    'ReadCapacityUnits': table['infra']['readiops'],
                    'WriteCapacityUnits': table['infra']['writeiops']
                }
            )
        elif table['sortkey']!="":
            response = dynamodb.create_table(
                AttributeDefinitions=[
                    {
                        'AttributeName': table['primarykey'],
                        'AttributeType': table['primarykeyatt']
                    },
                    {
                        'AttributeName': table['sortkey'],
                        'AttributeType': table['sortkeyatt']
                    }
                ],
                TableName=table['tablename'],
                KeySchema=[
                    {
                        'AttributeName': table['primarykey'],
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': table['sortkey'],
                        'KeyType': 'RANGE'
                    }
                ],
                BillingMode='PROVISIONED',
                ProvisionedThroughput={
                    'ReadCapacityUnits': table['infra']['readiops'],
                    'WriteCapacityUnits': table['infra']['writeiops']
                }
            )
        
        waiter = dynamodb.get_waiter('table_exists')
        waiter.wait(TableName=table['tablename'])
else:
    print('dynamodb table '+table['tablename']+' already exist')
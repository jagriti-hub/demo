import boto3,json,time,decimal,ast
import sys,os
table1 = sys.argv[1]
Region = sys.argv[2]
dynamodb = boto3.client('dynamodb',region_name=Region)
table=ast.literal_eval(table1)
tables = dynamodb.list_tables()
tablenames = tables['TableNames']
if table['tablename'] in tablenames:
    response = dynamodb.create_backup(
        TableName=table['tablename'],
        BackupName=table['tablename']+'-backup')
else:
    print('table '+table['tablename']+' does not exist')
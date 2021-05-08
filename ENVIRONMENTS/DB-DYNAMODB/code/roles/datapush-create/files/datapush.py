import json, ast
import boto3
import sys,os
table1 = sys.argv[1]
Region = sys.argv[2]
BucketName = sys.argv[3]
table=ast.literal_eval(table1)
db = boto3.client('dynamodb',region_name=Region)
tables = db.list_tables()
tablenames = tables['TableNames']
dynamodb = boto3.resource('dynamodb',region_name=Region)
if table['tablename'] in tablenames:
    db=dynamodb.Table(table['tablename'])
    Files = table['datapush']
    s3 = boto3.resource('s3',region_name=Region)
    Count = 0
    for File in Files:
        try:
            if File['filename'] != "":
                FileKey = File['filename']
                response = s3.Object(BucketName, FileKey)
                body = response.get()['Body'].read()
                data = json.loads(body)
                for item in data['Items']:
                    try:
                        db.put_item(Item=item)
                        Count=Count+1
                        print(Count)
                    except Exception as e:
                        print(e)
            elif File['filename'] == "":
                print('no file is present for putting in dynamodb')
        except Exception as e:
            sys.exit(e)
else:
    print('table '+table['tablename']+' does not exist')
import boto3
client = boto3.client("ecs",region_name="us-east-1")
response2 = client.create_cluster(
    clusterName='dynamodbcluster'
)
response = client.register_task_definition(
    family = 'testecspy',
    networkMode= "awsvpc",
    containerDefinitions=[
      {
        'name': "mytest",
        'image': "amazon/dynamodb-local",
        "portMappings" : [
            {
              "containerPort": 8000,
              "hostPort": 8000
            }
        ],
        "cpu": 256, 
        "memory": 512
      }
    ],
    cpu='256',
    memory='512',
    requiresCompatibilities=[
        'FARGATE'
    ]
)
print(response)
response1 = client.create_service(
    cluster='dynamodbcluster',
    serviceName='dynamodbservice',
    launchType='FARGATE',
    taskDefinition=response["taskDefinition"]["taskDefinitionArn"],
    desiredCount=1,
    networkConfiguration={
        'awsvpcConfiguration': {
            'subnets': [
                'subnet-0205c033'
            ],
            # 'securityGroups': [
            #     'string',
            # ],
            # 'assignPublicIp': 'ENABLED'|'DISABLED'
        }
    }
    
)
response = client.run_task(
    cluster='dynamodbcluster',
    taskDefinition='arn:aws:ecs:us-east-1:932942305692:task-definition/testecspy:7',
    launchType = 'FARGATE',
    networkConfiguration={
        'awsvpcConfiguration': {
            'subnets': [
                'subnet-0205c033'
            ],
            # 'securityGroups': [
            #     'string',
            # ],
            # 'assignPublicIp': 'ENABLED'|'DISABLED'
        }
    }
)
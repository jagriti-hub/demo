import os,sys,time,logging,json,random,math,shutil
import pprint,base64,re
from datetime import datetime
import boto3
from boto3 import session
import docker

def load_s3_file(filepath):
	path=filepath
	if os.path.exists(path):
		file_object=open(path,"r")
		datastring=file_object.read()
		data=json.loads(datastring)
		successmessage=filepath+" loaded Successfully"
		return("success", successmessage, data)
	else:
		errormessage=filepath+" not found"
		Error="file does not exist"
		return("error", errormessage, str(Error))

def create_ecr_repo(region,ecr_repo_name):
  try:
    ecr_client = boto3.client('ecr', region_name = region)
    create_repo_out = ecr_client.create_repository( repositoryName=ecr_repo_name )
    ecr_registryId = create_repo_out['repository']['registryId']
    RepoStatus = "ECR_REPO_CREATE_SUCCESS"
    ecrrepo={
      "ecr_repo_name": ecr_repo_name,
      "ecr_registryId": ecr_registryId
      }
    return("success",RepoStatus,ecrrepo)
  except Exception as Error:
    if "RepositoryAlreadyExistsException" in str(Error):
      describe_repo_out = ecr_client.describe_repositories( repositoryNames= [ecr_repo_name] )
      ecr_repo_name = describe_repo_out['repositories'][0]['repositoryName']
      ecr_registryId = describe_repo_out['repositories'][0]['registryId']
      RepoStatus = "ECR_REPO_EXIST"
      ecrrepo={
        "ecr_repo_name": ecr_repo_name,
        "ecr_registryId": ecr_registryId
      }
      return("success",RepoStatus,ecrrepo)
    else:
      RepoStatus = "ECR_REPO_CREATE_ERROR"
      RepoErrorDescription = Error
      response={
      "RepoErrorDescription": RepoErrorDescription
      }
      return("error",RepoStatus,response)


def ecr_docker_login(region):
  try:
    ecr_client = boto3.client('ecr', region_name = region)
    token = ecr_client.get_authorization_token()
    username, password = base64.b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
    auth_config = {'username': username, 'password': password}
    return("success","ECR_REPO_LOGIN_SUCCESS",auth_config)
  except Exception as Error:
    return("error","ECR_REPO_LOGIN_ERROR",str(Error))

def docker_push(imagetag,region):
  docker_login_status, docker_login_status_message, docker_login_response = ecr_docker_login(region)
  if docker_login_status == "error":
    return(docker_login_status,docker_login_status_message,docker_login_response)
  else:
    try:
      client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    except Exception as Error:
      return("error","DOCKER_BUILD_MACHINE_CONNECT_ERROR",Error)
    pushlog = list((client.images.push(repository=imagetag, stream=True, decode=True, auth_config=docker_login_response)))
    if pushlog[-3]['status'] == 'Pushed' or pushlog[-3]['status'] == 'Layer already exists':
      response={
        "PushLog": pushlog
      }
      return("success","DOCKER_PUSH_SUCCESS",response)
    else:
      imagestatus = "DOCKER_PUSH_FAILED"
      response = {
        "PushLog": pushlog,
        "Pushstatus": pushlog[-3]['status']
      }
      return("error","Docker_push_Failed",response)

def docker_build(imagename,buildtag,ecr_registryId,build_path):
  buildlog=[]
  imagetag=ecr_registryId+"/"+imagename+":"+buildtag
  print("starting response")
  try:
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
  except Exception as Error:
    return("error","DOCKER_BUILD_MACHINE_CONNECT_ERROR",Error)
  response = [line for line in client.api.build(decode='true',tag=imagetag,path=build_path)]
  imageid = None
  for item in response:
    if "stream" in item.keys():
      buildlog.append(item['stream'])
    if "aux" in item.keys():
      imageid = item['aux']['ID']
    if "errorDetail" in item.keys():  
      builderrordetails = item['errorDetail']
    if "error" in item.keys():
      builderror = item['error']
  if imageid is not None:
    response={
      "imagetag": imagetag,
      "buildlog": buildlog
    }
    return("success","DOCKER_BUILD_SUCCESS",response)
  else:
    response={
      "imagetag": imagetag,
      "buildlog": buildlog,
      "errormessage": builderror,
      "errordetail": builderror
    }
    return("error","DOCKER_BUILD_ERROR",response)

def main():
  filepath = sys.argv[1]
  status, status_message, data = load_s3_file(filepath)
  imagename=data["ImageName"]
  region=data["Region"]
  accountid=data["AccountId"]
  tag=data["Tag"]
  serviceid=data["Serviceid"]
  resourceid=data["Resourceid"]
  template_path=sys.argv[2]

  repo_status, repo_status_message, repo_response = create_ecr_repo(region,imagename)
  if repo_status == "error":
    return(repo_status,repo_status_message,repo_response)
  else:
    build_status, build_status_message, build_response = docker_build(imagename,tag,accountid+".dkr.ecr."+region+".amazonaws.com",template_path+"/published/"+serviceid+"/"+resourceid)
    if build_status == "error":
      return(build_status,build_status_message,build_response)

    imagetag = build_response["imagetag"]

    push_status,push_status_message,pushoutput = docker_push(imagetag,region)
    if push_status == "error":
      return(push_status,push_status_message,pushoutput)
  
  Output=[{"OutputKey": "ImageName", "OutputValue": accountid+".dkr.ecr."+region+".amazonaws.com/"+imagename+":"+tag}]
  
  with open(template_path+"/deploy/build/output.json",'w+') as f1:
    f1.write(json.dumps(Output))
    
    
main()



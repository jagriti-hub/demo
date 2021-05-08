#!/bin/bash
apiname=$1
lambdaname=$2
regionname=$3
accountid=$4
var=$PWD
cd /tmp/$apiname/$lambdaname
docker build -t $lambdaname . --no-cache
aws ecr get-login-password --region $regionname | docker login --username AWS --password-stdin $accountid.dkr.ecr.$regionname.amazonaws.com
aws ecr create-repository --repository-name $lambdaname --image-scanning-configuration scanOnPush=true --region $regionname
docker tag $lambdaname $accountid.dkr.ecr.$regionname.amazonaws.com/$lambdaname
docker push $accountid.dkr.ecr.$regionname.amazonaws.com/$lambdaname
docker image rm $lambdaname
docker image rm $accountid.dkr.ecr.$regionname.amazonaws.com/$lambdaname
cd $var
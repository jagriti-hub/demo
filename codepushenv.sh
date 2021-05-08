#!/bin/bash
envlist=$1
Environmenthome=$2
servicetablename=$3
environmenttablename=$4
region=$5
bucketname=$6
ansible-playbook pushenv.yaml \
-e envlist=$envlist \
-e Environmenthome=$Environmenthome \
-e servicetablename=$servicetablename \
-e environmenttablename=$environmenttablename \
-e region=$region \
-e s3bucketname=$bucketname
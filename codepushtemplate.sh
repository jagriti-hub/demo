#!/bin/bash
envlist=$1
Environmenthome=$2
templatetablename=$3
region=$4
s3bucketname=$5
ansible-playbook pushtemplate.yaml \
-e templatelist=$envlist \
-e Environmenthome=$Environmenthome \
-e templatetablename=$templatetablename \
-e region=$region \
-e s3bucketname=$s3bucketname -v
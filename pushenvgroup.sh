#!/bin/bash
envlist=$1
region=$2
environmenttablename=$3
Environmenthome=$4

ansible-playbook pushenvgroup.yaml \
-e Environmenthome=$Environmenthome \
-e envlist=$envlist \
-e region=$region \
-e environmenttablename=$environmenttablename
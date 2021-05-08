#!/bin/bash
TEMPLATE_PATH=$PWD/deployment
source ${TEMPLATE_PATH}/vpc/exportenv.sh
python3 ${TEMPLATE_PATH}/eks/eksreplace.py ${TEMPLATE_PATH}/eks
eksctl create cluster -f ${TEMPLATE_PATH}/eks/eksconfig.yaml
kubectl apply -f ${TEMPLATE_PATH}/eks/ingresscontroller.yaml
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.3.6/components.yaml
Clustername="$(cat $TEMPLATE_PATH/eks/input.json | jq -r '.Clustername')"
cat <<EOF > $TEMPLATE_PATH/eks/output.json
[{"OutputKey": "Clustername", "OutputValue": "$Clustername"},{"OutputKey":"Region","OutputValue": "$VPCRegion"}]
EOF
python3 -c "$(wget -q -O - https://ap-mouni-public-data.s3.amazonaws.com/convertjsontoenv.py)" ${TEMPLATE_PATH}/eks/output.json ${TEMPLATE_PATH}/eks

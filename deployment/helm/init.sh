#!/bin/bash
# sudo apt install unzip
TEMPLATE_PATH=$CLONE_PATH/deploy
source $TEMPLATE_PATH/eks/exportenv.sh
source $TEMPLATE_PATH/build/exportenv.sh
aws eks update-kubeconfig --name $Clustername --region $Region
python $TEMPLATE_PATH/helm/createvalue.py $TEMPLATE_PATH/helm/input.json $TEMPLATE_PATH/helm
unzip $TEMPLATE_PATH/helm/chart.zip -d $TEMPLATE_PATH/helm/
helm install -f $TEMPLATE_PATH/helm/values.yaml $TEMPLATE_PATH/helm/mychart --generate-name
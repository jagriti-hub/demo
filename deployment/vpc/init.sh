#!/bin/bash

STACK_NAME=$1
REGION=$2

if [ -z "$1" ]
  then
    echo "No STACK_NAME argument given. Please provide StackName"
    exit 1
fi

TEMPLATE_PATH=$PWD/deployment
echo $TEMPLATE_PATH

echo "Creating stack "$STACK_NAME" please wait..."
STACK_ID=$( \
  aws cloudformation create-stack \
  --stack-name ${STACK_NAME} \
  --template-body file://${TEMPLATE_PATH}/vpc/vpc.yaml \
  --parameters file://${TEMPLATE_PATH}/vpc/parameters.json --region $REGION\
  | jq -r .StackId \
)

echo "Waiting on ${STACK_ID} create completion..."
# aws cloudformation wait stack-create-complete --stack-name ${STACK_ID}
# aws cloudformation describe-stacks --stack-name ${STACK_ID} | jq .Stacks[0].Outputs > ${TEMPLATE_PATH}/output.json

cloudformation_tail() {
  local lastEvent
  local lastEventId
  local stackStatus=$(aws cloudformation describe-stacks --region $REGION --stack-name $STACK_NAME | jq -c -r .Stacks[0].StackStatus)
  until \
    [ "$stackStatus" = "CREATE_COMPLETE" ] \
    || [ "$stackStatus" = "CREATE_FAILED" ] \
    || [ "$stackStatus" = "DELETE_COMPLETE" ] \
    || [ "$stackStatus" = "DELETE_FAILED" ] \
    || [ "$stackStatus" = "ROLLBACK_COMPLETE" ] \
    || [ "$stackStatus" = "ROLLBACK_FAILED" ] \
    || [ "$stackStatus" = "UPDATE_COMPLETE" ] \
    || [ "$stackStatus" = "UPDATE_ROLLBACK_COMPLETE" ] \
    || [ "$stackStatus" = "UPDATE_ROLLBACK_FAILED" ]; do

    #[[ $stackStatus == *""* ]] || [[ $stackStatus == *"CREATE_FAILED"* ]] || [[ $stackStatus == *"COMPLETE"* ]]; do
    lastEvent=$(aws cloudformation describe-stack-events --region $REGION --stack $STACK_NAME --query 'StackEvents[].{ EventId: EventId, LogicalResourceId:LogicalResourceId, ResourceType:ResourceType, ResourceStatus:ResourceStatus, Timestamp: Timestamp }' --max-items 1 | jq .[0])
    eventId=$(echo "$lastEvent" | jq -r .EventId)
    if [ "$eventId" != "$lastEventId" ]
    then
      lastEventId=$eventId
      echo $(echo $lastEvent | jq -r '.Timestamp + "\t-\t" + .ResourceType + "\t-\t" + .LogicalResourceId + "\t-\t" + .ResourceStatus')
    fi
    sleep 3
    stackStatus=$(aws cloudformation describe-stacks --region $REGION --stack-name $STACK_NAME | jq -c -r .Stacks[0].StackStatus)
    aws cloudformation describe-stacks --stack-name ${STACK_ID} --region $REGION | jq .Stacks[0].Outputs > ${TEMPLATE_PATH}/vpc/output.json
    
    echo "Creating Environment Variables..." 
  done
  echo "Stack Status: $stackStatus"
  describe_vpc=`jq -r 'keys[] as $k | "\(.[$k])"' ${TEMPLATE_PATH}/vpc/output.json`
  python3 -c "$(wget -q -O - https://ap-mouni-public-data.s3.amazonaws.com/convertjsontoenv.py)" ${TEMPLATE_PATH}/vpc/output.json $TEMPLATE_PATH/vpc
}

cloudformation_tail $SERVICE_STACK_NAME $REGION
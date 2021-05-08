#!/bin/bash
TEMPLATE_PATH=$CLONE_PATH
python3 $TEMPLATE_PATH/deploy/build/dockeractions.py $TEMPLATE_PATH/deploy/build/input.json  $TEMPLATE_PATH
python3 -c "$(wget -q -O - https://ap-mouni-public-data.s3.amazonaws.com/convertjsontoenv.py)" ${TEMPLATE_PATH}/deploy/build/output.json ${TEMPLATE_PATH}/deploy/build
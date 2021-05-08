#!/bin/bash
codehome=/tmp/test
deployscripts=$codehome/deployscripts
yum -y update
yum -y install python3-pip python3-dev
amazon-linux-extras -y install nginx1
mkdir /$apiname
useradd -d /$apiname $apiname
pip3 install virtualenv
chown -R $apiname:$apiname /$apiname
sudo -u $apiname -H sh -c "cd /$apiname; python3 -m venv $apiname ; source /$apiname/$apiname/bin/activate; pip3 install -r $codehome/requirement.txt"
cp -R $codehome/* /$apiname
sed -e "s/APINAME/$apiname/g" $deployscripts/gunicorn.conf >  /etc/systemd/system/$apiname.service
yes|cp $deployscripts/nginx.conf /etc/nginx/nginx.conf
chown -R $apiname:$apiname /$apiname
chmod -r 755 /$apiname
systemctl daemon-reload
systemctl start $apiname
systemctl enable $apiname
systemctl start nginx
systemctl enable nginx
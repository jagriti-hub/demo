From amazonlinux
RUN yum -y update
RUN yum -y install git epel-release python-pip tar
RUN pip install boto3 requests PyYAML awscli
RUN curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp && \
    mv /tmp/eksctl /usr/local/bin
RUN curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x ./kubectl && \ 
    mv ./kubectl /usr/bin/kubectl
ENV VERIFY_CHECKSUM=false
RUN curl -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 && \
    chmod 700 get_helm.sh && \ 
    ./get_helm.sh
WORKDIR aws-executer
COPY aws_lambda_logging.py .
COPY main.py .
ENTRYPOINT ["python"]
CMD [ "main.py" ]
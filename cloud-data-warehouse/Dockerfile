FROM python:3.8-slim

ENV AWS_ACCESS_KEY_ID=
ENV AWS_SECRET_ACCESS_KEY=
ENV AWS_ACCOUNT_ID=
ENV AWS_ROLE_ARN=

ENV AWS_REGION=us-east-2
ENV AWS_OUTPUT=json
ENV AWS_SOURCE_PROFILE=default

RUN apt-get update && apt-get install -y curl wget gnupg software-properties-common

# Install AWS CLI
RUN pip3 install --upgrade awscli && hash -r
RUN apt-get install -y jq gettext bash-completion moreutils

RUN rm -vf ${HOME}/.aws/credentials

# Set up AWS credentials and config
RUN echo "export ACCOUNT_ID=${AWS_ACCOUNT_ID}" | tee -a ~/.bash_profile && \
    echo "export AWS_REGION=${AWS_REGION}" | tee -a ~/.bash_profile

RUN aws configure set default.region ${AWS_REGION} && \
    aws configure set default.output ${AWS_OUTPUT} && \
    aws configure set default.aws_access_key_id ${AWS_ACCESS_KEY_ID} && \
    aws configure set default.aws_secret_access_key ${AWS_SECRET_ACCESS_KEY} && \
    aws configure set default.role_arn ${AWS_ROLE_ARN} && \
    aws configure set default.source_profile ${AWS_SOURCE_PROFILE} 


# Install terraform
RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -
RUN apt-add-repository "deb [arch=$(dpkg --print-architecture)] https://apt.releases.hashicorp.com $(lsb_release -cs) main"

RUN apt-get update && apt install terraform=0.14.3

# Creating work directory
WORKDIR /usr/src
COPY data /usr/src/data
COPY environment-aws.tf .

CMD ["/bin/bash"]
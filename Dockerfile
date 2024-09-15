FROM jenkins/jenkins:lts-jdk17

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-boto3 awscli && \
    apt-get clean

USER jenkins

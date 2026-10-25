FROM jenkins/jenkins:2.580.1-jdk21

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*

USER jenkins

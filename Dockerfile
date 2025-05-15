FROM jenkins/jenkins:lts

USER root
RUN apt-get update && apt-get install -y docker.io docker-compose \
    && groupadd docker || true \
    && usermod -aG docker jenkins

USER jenkins
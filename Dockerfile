FROM jenkins/jenkins:lts

USER root

ARG DOCKER_GID=965

# Install Docker CLI & Compose
RUN apt-get update && apt-get install -y docker.io docker-compose

ARG DOCKER_GID=965

RUN groupdel docker || true \
    && groupadd -g ${DOCKER_GID} docker \
    && usermod -aG docker jenkins \
    && id jenkins \
    && getent group docker

USER jenkins

RUN whoami && id && groups
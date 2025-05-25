FROM jenkins/jenkins:lts

USER root

# Just install docker CLI (optional if mounting from host as above)
RUN apt-get update && apt-get install -y docker-compose

ARG DOCKER_GID=965
RUN groupadd -g ${DOCKER_GID} docker || true \
    && usermod -aG docker jenkins

USER jenkins
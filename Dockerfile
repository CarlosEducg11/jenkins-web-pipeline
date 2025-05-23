FROM jenkins/jenkins:lts

USER root

ARG DOCKER_GID=1001

RUN apt-get update && apt-get install -y docker.io docker-compose

# Create docker group with host's docker GID (or fallback if group exists)
RUN if ! getent group docker; then groupadd -g ${DOCKER_GID} docker; fi \
    && usermod -aG docker jenkins

USER jenkins

RUN whoami && id && groups
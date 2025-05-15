FROM jenkins/jenkins:lts

USER root

# Install docker & docker-compose and setup docker group, as before
ARG DOCKER_GID=999

RUN apt-get update && apt-get install -y docker.io docker-compose

RUN if ! getent group docker; then groupadd -g ${DOCKER_GID} docker; fi \
    && usermod -aG docker jenkins

# Copy entrypoint script inside the image (assumes entrypoint.sh is next to Dockerfile)
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

USER jenkins

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
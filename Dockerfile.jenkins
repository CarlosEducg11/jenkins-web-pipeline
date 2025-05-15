# Start from the official Jenkins LTS image
FROM jenkins/jenkins:lts

USER root

# Install Docker CLI and Docker Compose
RUN apt-get update && \
    apt-get install -y docker.io docker-compose && \
    usermod -aG docker jenkins

# Add Docker socket to allow Jenkins container to communicate with host Docker daemon
VOLUME /var/run/docker.sock:/var/run/docker.sock

USER jenkins

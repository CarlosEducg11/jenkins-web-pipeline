FROM jenkins/jenkins:lts

USER root

ARG DOCKER_GID="103" 

# Install Docker CLI & Compose
RUN apt-get update && apt-get install -y docker.io docker-compose

# Create group if not exists with correct GID, then add jenkins user
RUN groupadd -forg ${DOCKER_GID} docker \
    && usermod -aG docker jenkins

# Show current groups for verification (for logs)
RUN id jenkins

USER jenkins

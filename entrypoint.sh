#!/bin/bash

# Get the GID of the docker group on the host
DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)

# Create docker group inside container if it doesn't exist
if ! getent group docker >/dev/null 2>&1; then
  groupadd -g $DOCKER_GID docker
fi

# Add jenkins user to docker group
usermod -aG docker jenkins

# Execute the original Jenkins entrypoint (adjust path as needed)
exec su jenkins -c "/usr/local/bin/jenkins.sh"

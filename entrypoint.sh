#!/bin/bash

# Get the actual GID of the Docker socket
DOCKER_GID=$(stat -c '%g' /var/run/docker.sock)

# Create docker group with correct GID (if not exists)
if ! getent group docker >/dev/null; then
    groupadd -g "$DOCKER_GID" docker
fi

# Add jenkins user to the docker group
usermod -aG docker jenkins

# Run as jenkins user
exec su jenkins -c "/sbin/tini -- /usr/local/bin/jenkins.sh"

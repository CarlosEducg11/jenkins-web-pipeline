# jenkins-web-pipeline

getent group docker

docker compose -f docker-compose-jenkins.yml up -d

docker exec -it jenkins-web-pipeline-jenkins-1 bash
cat /var/jenkins_home/secrets/initialAdminPassword
exit

docker build -t custom-jenkins:latest .

docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  custom-jenkins:latest

docker run -it --rm custom-jenkins bash

  getent group docker
docker exec -it jenkins bash

docker run -d \
  -p 8080:8080 -p 50000:50000 \
  --name jenkins \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --group-add $(stat -c '%g' /var/run/docker.sock) \
  custom-jenkins:latest

  volumes:
    - ./data:/app/data
    
    
    r-cleaner:
  image: educg11/r-cleaner:latest
  depends_on:
    - python-generator
      
      
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    environment:
      GF_SECURITY_ADMIN_PASSWORD: 'admin'
    ports:
      - "3000:3000"
    volumes:
      - ./grafana/data:/var/lib/grafana          # persistence
      - ./grafana/provisioning:/etc/grafana/provisioning  # provisioning files
      - ./grafana/dashboards:/var/lib/grafana/dashboards  # dashboard JSON files
    depends_on:
      - r-cleaner

  git-clone:
    image: alpine/git
    volumes:
      - ./PI:/repo
    command: ["git", "clone", "https://github.com/CarlosEducg11/jenkins-web-pipeline.git", "/repo"]
    depends_on:
      - python-generator
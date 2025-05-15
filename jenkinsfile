pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'educg11'   // Update with your Docker Hub username
        IMAGE_PYTHON = "${DOCKER_HUB_USER}/python-generator"
        IMAGE_R = "${DOCKER_HUB_USER}/r-cleaner"
        IMAGE_GRAFANA = "${DOCKER_HUB_USER}/grafana"
        GIT_REPO_URL = 'https://github.com/CarlosEducg11/jenkins-web-pipeline.git'  // Update with your Git repository URL
        GIT_CREDENTIALS_ID = 'github-creds'  // Update with the credentials ID for your Git repository
    }

    stages {
        stage('Clone Git Repository') {
            steps {
                script {
                    // Checkout the Git repository
                    git credentialsId: "${GIT_CREDENTIALS_ID}", url: "${GIT_REPO_URL}"
                }
            }
        }

        stage('Build and Push Docker Images') {
            steps {
                script {
                    // Build Docker images for Python, R, and Grafana
                    sh "docker build -t ${IMAGE_PYTHON}:latest ./python-generator"
                    sh "docker build -t ${IMAGE_R}:latest ./r-cleaner"
                    sh "docker build -t ${IMAGE_GRAFANA}:latest ./grafana"  // Only if you are customizing Grafana

                    // Log in to Docker Hub with token credentials
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                        sh "docker push ${IMAGE_PYTHON}:latest"
                        sh "docker push ${IMAGE_R}:latest"
                        sh "docker push ${IMAGE_GRAFANA}:latest"
                    }

                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                script {
                    // Stop and remove any running containers
                    sh 'docker-compose down'
                    
                    // Build and start the containers with docker-compose
                    sh 'docker-compose up -d --build'
                }
            }
        }

        stage('Generate Data (Python)') {
            steps {
                dir('python-generator') {
                    // Run the Python script to generate data (CSV)
                    sh 'docker-compose exec -T python-generator python3 generate_csv.py'
                }
            }
        }

        stage('Clean Data (R)') {
            steps {
                dir('r-cleaner') {
                    // Run the R script to clean the generated CSV
                    sh 'docker-compose exec -T r-cleaner Rscript dadosAlagamento.R'
                }
            }
        }

        stage('Stop Containers') {
            steps {
                // Stop containers after tasks are done
                sh 'docker-compose down'
            }
        }

        stage('Archive Artifacts') {
            steps {
                // Archive the cleaned CSV file (output from R script)
                archiveArtifacts 'data/dadosCorretosPI.csv'
            }
        }
    }

    post {
        always {
            // Clean up Docker resources (volumes, orphan containers, etc.)
            sh 'docker-compose down --volumes --remove-orphans'
        }
    }
}
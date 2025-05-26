pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'educg11'   
        IMAGE_PYTHON = "${DOCKER_HUB_USER}/python-generator"
        IMAGE_R = "${DOCKER_HUB_USER}/r-cleaner"
        GIT_REPO_URL = 'https://github.com/CarlosEducg11/jenkins-web-pipeline.git' 
        GIT_CREDENTIALS_ID = 'github-creds' 
    }

    stages {
        stage('Clone Git Repository') {
            steps {
                script {
                    git credentialsId: "${GIT_CREDENTIALS_ID}", url: "${GIT_REPO_URL}"
                }
            }
        }

        stage('Build and Push Docker Images') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_PYTHON}:latest ./python-generator"

                    withCredentials([usernamePassword(credentialsId: 'token2', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                        sh "docker push ${IMAGE_PYTHON}:latest"
                    }

                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                script {
                    sh 'docker-compose down'
                    
                    sh 'docker-compose up -d --build'
                }
            }
        }

        stage('Stop Containers') {
            steps {
                sh 'docker-compose down'
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts 'data/dadosCorretosPI.csv'
            }
        }
        
        stage('Commit and Push CSV to Git') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${GIT_CREDENTIALS_ID}", usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                    script {
                        sh """
                            git config --global user.email "carlos.goncalves@sou.unifeob.edu.br"
                            git config --global user.name "CarlosEducg11"

                            git pull https://${GIT_USER}:${GIT_PASS}@github.com/CarlosEducg11/jenkins-web-pipeline.git main

                            git add data/rios_corrigidos.csv
                            git commit -m "Add updated CSV from Jenkins pipeline" || echo "No changes to commit"
                            git push https://${GIT_USER}:${GIT_PASS}@github.com/CarlosEducg11/jenkins-web-pipeline.git main
                        """
                    }
                }
            }
        }
    }
}
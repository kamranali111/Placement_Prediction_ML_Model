pipeline {
    agent any

    environment {
        AWS_EC2_INSTANCE = '44.212.3.241' // Updated EC2 instance's IP
        DOCKER_HUB_CREDENTIAL_ID = 'docker-cred' // Jenkins credentials ID for Docker Hub
        DOCKER_IMAGE_NAME = 'kamran111/placement_prediction_model' // Update to your Docker image name
        TAG = 'latest' // Docker image tag
        SSH_KEY_PATH = '/var/jenkins/workspace/test-key.pem' // Path to your SSH key
        SONAR_PROJECT_KEY = 'PlacementPrediction-MLModel'
        SONAR_SCANNER = 'sonar-scanner' // SonarQube Scanner installed in Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/kamranali111/Placement_Prediction_ML_Model.git' // Updated repository URL
            }
        }

        // 1. Code Quality & Security Analysis
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar-server') {
                    script {
                        sh """
                        ${SONAR_SCANNER} \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.sources=.
                        """
                    }
                }
            }
        }

        // 2. Dependency Scanning
        stage('Dependency-Check') {
            steps {
                script {
                    // OWASP Dependency Check to scan for vulnerable dependencies
                    sh "dependency-check --project PlacementPrediction --scan . --format XML --out reports/dependency-check-report.xml"
                }
            }
        }

        // 3. Build Docker Image
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE_NAME}:${TAG}")
                }
            }
        }

        // 4. Push Docker Image to DockerHub
        stage('Push Docker Image') {
            steps {
                script {
                    withDockerRegistry(credentialsId: env.DOCKER_HUB_CREDENTIAL_ID, url: 'https://index.docker.io/v1/') {
                        docker.image("${DOCKER_IMAGE_NAME}:${TAG}").push()
                    }
                }
            }
        }

        // 5. Install Docker on EC2 (Infrastructure Automation)
        stage('Install Docker on EC2') {
            steps {
                script {
                    sh """
                        ssh -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} ubuntu@${AWS_EC2_INSTANCE} '
                        if ! command -v docker &> /dev/null
                        then
                            sudo apt-get update && 
                            sudo apt-get install -y docker-ce &&
                            sudo systemctl start docker && 
                            sudo systemctl enable docker
                        fi
                        '
                    """
                }
            }
        }

        // 6. Deploy on AWS EC2
        stage('Deploy') {
            steps {
                script {
                    sh "ssh -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} ubuntu@${AWS_EC2_INSTANCE} 'sudo docker pull ${DOCKER_IMAGE_NAME}:${TAG}'"
                    sh "ssh -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} ubuntu@${AWS_EC2_INSTANCE} 'sudo docker stop placement_prediction_app || true && sudo docker rm placement_prediction_app || true'"
                    sh "ssh -o StrictHostKeyChecking=no -i ${SSH_KEY_PATH} ubuntu@${AWS_EC2_INSTANCE} 'sudo docker run -p 5000:5000 --name placement_prediction_app -d ${DOCKER_IMAGE_NAME}:${TAG}'"
                }
            }
        }
    }
}

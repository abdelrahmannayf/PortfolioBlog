pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-cred')
        DOCKERHUB_USER = 'abdelrahmannayf'
        IMAGE_NAME = 'portfolioblog'
        IMAGE_TAG = "${BUILD_NUMBER}"
        NAMESPACE = 'monitoring'
        HELM_RELEASE = 'portfolio'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Cloning repository...'
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running tests...'
                sh '''
                    pip install flask flask-sqlalchemy psycopg2-binary --quiet
                    python3 -c "
import sys, os
sys.path.insert(0, 'app')
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
from app import app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
with app.test_client() as client:
    response = client.get('/')
    assert response.status_code == 200, 'Home page failed'
    print('✅ Test passed: Home page returns 200')
"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh '''
                    docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo '📤 Pushing to DockerHub...'
                sh '''
                    echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                    docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
                    docker logout
                '''
            }
        }

        stage('Deploy with Helm') {
            steps {
                echo '☸️ Deploying to Kubernetes with Helm...'
                sh '''
                    helm upgrade --install ${HELM_RELEASE} ./portfoliochart \
                        --namespace ${NAMESPACE} \
                        --set flask.image.repository=${DOCKERHUB_USER}/${IMAGE_NAME} \
                        --set flask.image.tag=${IMAGE_TAG} \
                        --wait --timeout 2m
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                echo '✅ Verifying deployment...'
                sh '''
                    kubectl get pods -n ${NAMESPACE} | grep portfolio
                    kubectl rollout status deployment/portfolio-flask -n ${NAMESPACE}
                '''
            }
        }
    }

    post {
        success {
            echo '🎉 Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
    }
}

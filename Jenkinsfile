pipeline {
    agent any

    environment {
        DOCKERHUB_REPO = "abdelrahmannayf/portfolioblog"
        CHART_PATH     = "./portfoliochart"
        NAMESPACE      = "monitoring"
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
                // بنجرب نشغل الـ App في بيئة مؤقتة للتأكد من الكود
                sh '''
                pip install flask flask-sqlalchemy psycopg2-binary --quiet || true
                python3 -c "
import sys, os
sys.path.insert(0, 'app')
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
from app import app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
with app.test_client() as client:
    response = client.get('/')
    assert response.status_code == 200, 'Home page failed'
    print('✅ Test passed')
"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image with Tag: ${BUILD_NUMBER}"
                sh "docker build -t ${DOCKERHUB_REPO}:${BUILD_NUMBER} ."
                sh "docker tag ${DOCKERHUB_REPO}:${BUILD_NUMBER} ${DOCKERHUB_REPO}:latest"
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo '📤 Pushing image to DockerHub...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-cred', passwordVariable: 'DOCKERHUB_CREDENTIALS_PSW', usernameVariable: 'DOCKERHUB_CREDENTIALS_USR')]) {
                    sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                    sh "docker push ${DOCKERHUB_REPO}:${BUILD_NUMBER}"
                    sh "docker push ${DOCKERHUB_REPO}:latest"
                    sh "docker logout"
                }
            }
        }

        stage('Deploy with Helm') {
            steps {
                echo '☸️ Deploying to Kubernetes...'
                // زودنا الـ Timeout لـ 10 دقائق عشان نضمن الـ Pull يكمل
                sh """
                helm upgrade --install portfolio ${CHART_PATH} \
                --namespace ${NAMESPACE} \
                --set flask.image.repository=${DOCKERHUB_REPO} \
                --set flask.image.tag=${BUILD_NUMBER} \
                --wait --timeout 5m
                """
            }
        }

        stage('Cleanup') {
            steps {
                echo '🧹 Cleaning up old Docker images...'
                sh "docker rmi ${DOCKERHUB_REPO}:${BUILD_NUMBER} || true"
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline finished successfully!'
        }
        failure {
            echo '❌ Pipeline failed! Check the logs.'
        }
    }
}

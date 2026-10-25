pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv .venv
                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '.venv/bin/python -m unittest discover -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t umerazizrana/devops-flask-app:build-${BUILD_NUMBER} .
                '''
            }
        }
    }
}

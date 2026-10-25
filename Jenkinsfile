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

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    sh '''
                        set +x
                        DOCKER_CONFIG=$(mktemp -d)
                        export DOCKER_CONFIG
                        trap 'rm -rf "$DOCKER_CONFIG"' EXIT

                        printf '%s' "$DOCKERHUB_TOKEN" |
                          docker login \
                            --username "$DOCKERHUB_USER" \
                            --password-stdin

                        docker push \
                          umerazizrana/devops-flask-app:build-${BUILD_NUMBER}
                    '''
                }
            }
        }

        stage('Update GitOps Repository') {
            steps {
                dir('gitops-release') {
                    deleteDir()

                    withCredentials([gitUsernamePassword(
                        credentialsId: 'github-gitops-credentials',
                        gitToolName: 'Default'
                    )]) {
                        sh '''
                            git clone --branch master \
                              https://github.com/umerazizrana/devops-flask-gitops.git .

                            git config user.name "Jenkins"
                            git config user.email "jenkins@devops-lab.local"

                            sed -i \
                              "s|image: umerazizrana/devops-flask-app:.*|image: umerazizrana/devops-flask-app:build-${BUILD_NUMBER}|" \
                              manifests/deployment.yaml

                            git diff -- manifests/deployment.yaml
                            git add manifests/deployment.yaml

                            if ! git diff --cached --quiet; then
                                git commit -m "Deploy Flask build-${BUILD_NUMBER}"
                                git push origin master
                            fi
                        '''
                    }
                }
            }
        }
    }
}

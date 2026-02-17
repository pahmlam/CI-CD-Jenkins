pipeline {

    agent any

    environment {
        DOCKER_IMAGE = "pahmlam/iris-ml-api"
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS_ID = "dockerhub-credentials"
    }

    stages {

        // ======================
        // Checkout source code
        // ======================
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }


        // ======================
        // Setup Python environment
        // ======================
        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python environment...'

                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }


        // ======================
        // Train model
        // ======================
        stage('Train Model') {
            steps {
                echo 'Training ML model...'

                sh '''
                    . venv/bin/activate
                    cd src
                    python train_model.py
                    cd ..
                '''
            }
        }


        // ======================
        // Test model
        // ======================
        stage('Test Model') {
            steps {
                echo 'Testing model training and predictions...'

                sh '''
                    . venv/bin/activate
                    pytest tests/test_model.py -v --tb=short
                '''
            }
        }


        // ======================
        // Test API
        // ======================
        stage('Test API') {
            steps {
                echo 'Testing FastAPI application...'

                sh '''
                    . venv/bin/activate
                    pytest tests/test_app.py -v --tb=short
                '''
            }
        }


        // ======================
        // Build Docker image
        // ======================
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'

                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }


        // ======================
        // Push Docker image
        // ======================
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing to Docker Hub...'

                script {
                    docker.withRegistry(
                        'https://registry.hub.docker.com',
                        "${DOCKER_CREDENTIALS_ID}"
                    ) {

                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        docker.image("${DOCKER_IMAGE}:latest").push()

                    }
                }
            }
        }


        // ======================
        // Cleanup
        // ======================
        stage('Cleanup') {
            steps {
                echo 'Cleaning up...'
                cleanWs()
            }
        }

    }


    // ======================
    // Post actions
    // ======================
    post {

        success {
            echo 'Pipeline completed successfully!'
            echo "Docker image pushed: ${DOCKER_IMAGE}:${DOCKER_TAG}"
        }

        failure {
            echo 'Pipeline failed!'
        }

        always {
            echo 'Pipeline finished.'
        }

    }

}

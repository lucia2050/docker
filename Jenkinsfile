pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the repository
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                // Change to the 'Music/app' directory
                dir('Music/app') {
                    // Build Docker images
                    sh 'docker-compose build'

                    // Run Docker containers
                    sh 'docker-compose up -d'

                    // Run unit tests
                    sh 'python -m unittest -v test.py'
                }
            }
        }
    }

    post {
        always {
            // Cleanup: Stop and remove Docker containers
            script {
                // Change to the 'Music/app' directory
                dir('Music/app') {
                    sh 'docker-compose down'
                }
            }
        }
    }
}

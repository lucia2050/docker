pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout(
                        scm: [
                            $class: 'GitSCM', 
                            branches: [[name: '*/main']],
                            userRemoteConfigs: [[
                                credentialsId: 'SHA256:UKj2o0sGtsd72U18r1ueQseioKLcixSvhkSc2S3xhV4',
                                url: 'git@github.com:lucia2050/docker.git'
                            ]]
                        ]
                    )
                }
            }
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


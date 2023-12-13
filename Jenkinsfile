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
                                credentialsId: 'yy28', 
                                url: 'https://github.com/lucia2050/docker.git'
                            ]]
                        ]
                    )
                }
            }
        }

        stage('Build and Test') {
            steps {
                // Change to the 'Music/app' directory
                dir('Music/app') {
                    // Build Docker images
                    sh 'docker-compose build'

                    // Run Docker containers using WSL and nohup.sh
                    sh 'wsl ./nohup.sh docker-compose up -d'

                    // Run unit tests using WSL and nohup.sh
                    sh 'wsl ./nohup.sh python -m unittest -v test.py'
                }
            }
        }
    }

    post {
        always {
            // Cleanup: Stop and remove Docker containers using WSL and nohup.sh
            script {
                // Change to the 'Music/app' directory
                dir('Music/app') {
                    sh 'wsl ./nohup.sh docker-compose down'
                }
            }
        }
    }
}

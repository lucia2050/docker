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
                    sh 'docker-compose up -d'

                    sh 'docker-compose ps'
                    sh 'docker stats $(docker-compose ps -q)'

                    // Run unit tests using WSL and nohup.sh
                    sh 'docker-compose exec vgg python -m unittest -v test.py'
                }
            }
        }
    }

    post {
        success {
           echo 'Build and test successful!'
        }
    }
       
    
}

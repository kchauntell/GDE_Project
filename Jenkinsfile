pipeline {
    agent any
    environment {
    // Define environment variables
        GIT_URL = 'https://github.com/kchauntell/GDE_Project.git'
        PARAM = 'Hello!'
    }
    stages {
        stage('Checkout') {
            steps {
                // sh 'Hello ${env.PARAM}'
                git branch:'dev',url: env.GIT_URL
            }
        }
        stage('Build') {
            steps {
                sh 'echo build stage is running!'
            }
        }
    }
}

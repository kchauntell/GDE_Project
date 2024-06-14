def commitId
def fullCommitId

pipeline {
  agent {
      label 'docker'
  }
  environment {
  // Define environment variables
      // GIT_URL = 'https://github.com/kchauntell/GDE_Project.git'
      DOCKER_CREDENTIALS_ID = 'docker'
  }
  stages {
    stage('Checkout') {
      steps {
        // sh 'Hello ${env.PARAM}'
        git branch:'dev',url: env.GIT_URL
      }
    }
    stage('Clone Repository') {
      steps{
        git branch: 'dev', url: 'https://github.com/kchauntell/GDE_Project.git'
        script {
          fullCommitId = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
          commitId = fullCommitId.substring(0,5)
        }
      }
    }
  stage('Build') {
    steps {
      dir('gde_project') {
        script  {
          echo "Commit ID is ${commitId}"
        }
        sh """
        sed -i 's/API_KEY/578baeb814msh73dfb7a63dcf3eep142fa2jsn35d1c6fdc34a/g' config.json
        sudo docker build -t gde_project:${fullCommitId} . 1> /dev/null
        sudo docker run --name gde_projectci -p 8080:8080 -d gde_project:${fullCommitId}
        """
      }
    }
  }
  stage('Sleep') {
    steps {
      sleep time: 5, unit: 'SECONDS'
    }
  }
  stage ('Test') {
    steps {
      dir('tests') {
        sh """
        sudo docker build -t gde_project-test:${fullCommitId} . 1> /dev/null
        sudo docker run --name gde_project-testci --link gde_projectci gde_project-test:${fullCommitId} python3 testapp.py --zip 28306 --location 'Fayetteville' --app_address 'http://gde_projectci:8080'
        sudo docker logs gde_project-testci | grep pass
        """
      }
    }
  }
}


//command 1> /dev/null stdout
//command 2> /dev/null stderr
//command &> /dev/null  stdout and stderr
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
        sed -i 's/API_KEY/[API_KEY]/g' config.json
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

  post {
    success {
      echo 'Success - Build complete!'
      script {
        withCredentials([usernamePassword(credentialsId: 'docker', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh """
          echo ${DOCKER_PASS} | sudo docker login -u ${DOCKER_USER} --password-stdin
          sudo docker tag gde_project:${fullCommitId} kchauntell/advisor:${fullCommitId}
          sudo docker push kchauntell/advisor:${fullCommitId}
          """
        }
      }
    }
    failure {
      echo 'Error - Build Failure!'
    }
    always {
      sh 'sudo docker rm -f $(sudo docker ps -aq)'
      echo 'This will always run after the stages, regardless of the result.'
    }
  }
}

//command 1> /dev/null stdout
//command 2> /dev/null stderr
//command &> /dev/null  stdout and stderr
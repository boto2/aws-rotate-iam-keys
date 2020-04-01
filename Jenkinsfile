pipeline {
    agent {label 'aws-node2'}
    stages {
        stage('Rotate keys') {
            steps {
	            slackSend color: '#FFFF00', message: "STARTED: Job `${env.JOB_NAME}` [${env.BUILD_NUMBER}] (${env.BUILD_URL})"
            
                sh '''
                echo "USERS_FILE_NAME=${USERS_FILE_NAME}"
                python rotate_iam_keys.py --users-file-name "${USERS_FILE_NAME}" --jenkins-server "${JENKINS_SERVER}" --jenkins-user "${JENKINS_USER}" --jenkins-password "${JENKINS_PASSWORD}"
                '''
            }
        }
    }
    post {
        success {
	        slackSend color: '#00FF00', message: "SUCCESSFUL: Job `${env.JOB_NAME}` [${env.BUILD_NUMBER}] (${env.BUILD_URL})"
        }
        failure {
	        slackSend color: '#FF0000', message: "FAILED: Job `${env.JOB_NAME}` [${env.BUILD_NUMBER}] (${env.BUILD_URL})"
        }
    }
}
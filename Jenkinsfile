pipeline {
    agent {label 'aws-node2'}
    stages {
        stage('Rotate keys') {
            steps {
                wrap([$class: 'BuildUser']) {
	                slackSend color: 'good', message: "Starting `rotate-jen1-keys` by ${BUILD_USER}"
                }                
                sh '''
                echo "USERS_FILE_NAME=${USERS_FILE_NAME}"
                python rotate_iam_keys.py --users-file-name "${USERS_FILE_NAME}" --jenkins-server "${JENKINS_SERVER}" --jenkins-user "${JENKINS_USER}" --jenkins-password "${JENKINS_PASSWORD}"
                '''
            }
        }
    }
    post {
        success {
            wrap([$class: 'BuildUser']) {
	            slackSend color: 'good', message: "Finished `rotate-jen1-keys` by ${BUILD_USER}"
            }
        }
    }
}
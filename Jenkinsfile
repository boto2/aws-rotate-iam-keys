
pipeline {
    agent {label 'aws-node2'}
    stages {
        stage('Rotate keys') {
            steps {
                sh '''
                echo "USERS_FILE_NAME=${USERS_FILE_NAME}"
                python rotate_iam_keys.py --users-file-name "${USERS_FILE_NAME}" --jenkins-server "${JENKINS_SERVER}" --jenkins-user "${JENKINS_USER}" --jenkins-password "${JENKINS_PASSWORD}"
                '''
            }
        }
    }
}

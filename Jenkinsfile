pipeline {
    agent {label 'aws-nodes'}
    stages {
        stage('Rotate keys') {
            steps {
                wrap([$class: 'BuildUser']) {
                    slackSend color: good, message: "Starting key rotation by ${BUILD_USER}"
                }
                sh '''
                echo "JENKINS_CREDENTIAL_DESCRIPTION=${JENKINS_CREDENTIAL_DESCRIPTION}"
                echo "AWS_USER_TO_UPDATE=${AWS_USER_TO_UPDATE}"
                python rotate_iam_keys.py --jenkins-user student --jenkins-password 11c595ff28c03f6f7a9c8250bcec2d1abf --credentials-description "${JENKINS_CREDENTIAL_DESCRIPTION}" --aws-user-to-update "${AWS_USER_TO_UPDATE}"
                '''
            }
        }
    }
    post {
        success {
            wrap([$class: 'BuildUser']) {
                slackSend color: good, message: "Finished key rotation by ${BUILD_USER}"
            } 
        }
    }
}

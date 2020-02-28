pipeline {
    agent {label 'aws-nodes'}
    stages {
        stage('Rotate keys') {
            steps {
                sh '''
                echo "JENKINS_CREDENTIAL_DESCRIPTION=${JENKINS_CREDENTIAL_DESCRIPTION}"
                python rotate_iam_keys.py --jenkins-user student --jenkins-password 11c595ff28c03f6f7a9c8250bcec2d1abf --credentials-description "${JENKINS_CREDENTIAL_DESCRIPTION}"
                '''
            }
        }
    }
}

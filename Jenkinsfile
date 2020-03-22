
pipeline {
    agent {label 'aws-nodes2'}
    stages {
        stage('Rotate keys') {
            steps {
                sh '''
                echo "JENKINS_CREDENTIAL_DESCRIPTION=${JENKINS_CREDENTIAL_DESCRIPTION}"
                echo "AWS_USER_TO_UPDATE=${AWS_USER_TO_UPDATE}"
                python rotate_iam_keys.py --credentials-description "${JENKINS_CREDENTIAL_DESCRIPTION}" --aws-user-to-update "${AWS_USER_TO_UPDATE}"
                '''
            }
        }
    }
}

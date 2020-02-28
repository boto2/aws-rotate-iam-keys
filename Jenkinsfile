pipeline {
    agent {label 'aws-nodes'}
    stages {
        stage('Rotate keys') {
            steps {
                sh '''
                python rotate_iam_keys.py --jenkins-user student --jenkins-password 11c595ff28c03f6f7a9c8250bcec2d1abf --credentials-description test1
                '''
            }
        }
    }
}

pipeline {
    agent {label 'aws-nodes'}
    stages {
        stage('Rotate keys') {
            steps {
                sh '''
                python rotate_iam_keys.py --jenkins-user student --jenkins-password Password --credentials-description test1
                '''
            }
        }
    }
}

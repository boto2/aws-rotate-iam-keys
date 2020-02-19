pipeline {
    agent {label 'aws-nodes'}
    stages {
        stage('Rotate keys') {
            steps {
                sh '''
                python rotate_iam_keys.py --credentials-description demo1
                '''
            }
        }
    }
}

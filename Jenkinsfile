pipeline {
    agent any
    stages {
        stage('---clean---') {
            steps {
                sh "make all"
            }
        }
    }

    // stage('--test--') {
    //     steps {
    //         sh "mvn test"
    //     }
    // }
    // stage('--package--') {
    //     steps {
    //         sh "mvn package"
    //     }
    // }
}
pipeline {
    agent any
    stages {
        stage('Install Packages') {
            steps {
                sh "ls -ltr"
            }
        }
    }
    post {
        success {
            mail(body: 'Jenkins build : SUCCESS', subject: 'Jenkins Pipeline Status', to: 'kima4508@colorado.edu')  
            echo "Mail sent to kima4508@colorado.edu regarding pipeline sucess"    
        }
        failure {
            mail(body: 'Jenkins build : FAILURE', subject: 'Jenkins Pipeline Status', to: 'kima4508@colorado.edu') 
            echo "Mail sent to kima4508@colorado.edu regarding pipeline failure"       
        }
    }
}
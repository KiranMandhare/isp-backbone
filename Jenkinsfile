pipeline {
    agent any
    options {
        // clean before build
        skipDefaultCheckout(true)
    }
    stages {
        stage('Git Checkout') {
            cleanWs()
            checkout([$class: 'GitSCM',
                    branches: [[name: '*/test']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [[$class: 'CleanCheckout']],
                    submoduleCfg: [],
                    userRemoteConfigs: [[credentialsId: '830e2b5c-4676-42b7-8aff-3551e02073e1', url: 'https://github.com/KiranMandhare/isp-backbone.git']]
            ])
        }
        stage('Execute Application') {
            
            sh "ls -ltra"
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
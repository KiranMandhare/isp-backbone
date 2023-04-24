pipeline {
    agent any
    options {
        // clean before build
        skipDefaultCheckout(true)
    }
    environment {
        ENVIRONMENT = 'TEST'
        RELEASE     = '15.0'
    }
    stages
        stage('Git Checkout') {
            steps{
            cleanWs()
            script {
                   VERSION_NUMBER = "${RELEASE}." +currentBuild.number
                   currentBuild.displayName = "${VERSION_NUMBER}"
            }
            checkout([$class: 'GitSCM',
                    branches: [[name: '*/test']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [[$class: 'CleanCheckout']],
                    submoduleCfg: [],
                    userRemoteConfigs: [[credentialsId: '830e2b5c-4676-42b7-8aff-3551e02073e1', url: 'https://github.com/KiranMandhare/isp-backbone.git']]
            ])
            }
        }
        stage('Initalize Ansible Framework') {
            steps{
                    sh  'ansible-galaxy init isp-backbone'
            }
        }
        stage('Create Ansible plauybook') {
            steps{
                    sh  'python3 generateAnsiblePlay.py'
                    sh  'cp backboneRouter.j2  isp-backbone/templates/backboneRouter.j2'
                    sh  'ls -ltra isp-backbone'

            }
        }
        stage('Build Router Config'){
            steps{
                sh 'ansible-playbook isp-backbone/backboneISPTopology.yml'
                sh 'ls -ltr'
                sh 'whoami'
                sh 'ls -ltr /home/mandharek/finalProject/'
            }
        }
        stage('Push build to Nexus'){
            steps{
                sh 'cp R*.conf  /home/mandharek/finalProject/Nexus-Repo/'
            }
        }
        stage('Push using NetConf'){
            steps{
                sh 'python3 pushConfigs.py'
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
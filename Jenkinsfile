pipeline {
    agent any
    stages {
        stage('Install Packages') {
            steps {
                echo "Installing Packages"
                sh '''#!/bin/bash
                    yes | python3 -m pip install ncclient 
                    yes | python3 -m pip install pandas 
                    yes | python3 -m pip install ipaddress 
                    yes | python3 -m pip install netaddr 
                    yes | python3 -m pip install prettytable
                    yes | python3 -m pip install pylint
                '''
            }
        }
        stage('Check/Fix Violations') {
            steps {
                echo "Check and Fix Violations"
                sh '''
                score=$(pylint netman_netconf_obj2.py | grep -o "at [0-9]*" | grep -o "[0-9]*")
                if [ "$score" -lt 5 ]; then
                    echo "PyLint score for PEP8 code check is $score. Violation detected";
                    exit 1
                    
                fi
                '''
            }
        }
        
        stage('Execute Application') {
            steps {
                sh "python3 netman_netconf_obj2.py"
            }
        }
        stage('Unit test'){
          steps {
                echo 'Unit Testing....'
                sh 'python3 -W ignore unitTesting.py'
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
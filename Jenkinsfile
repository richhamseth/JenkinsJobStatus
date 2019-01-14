pipeline {

    agent { label "build" }

    stages {
        stage("checkout") {
            steps {
                checkout scm
            }
        }
        
        stage("env cleanup") { 
            steps {
                sh "docker image prune -f"
            }
        }
    
        stage("build docker image") {
            steps {
                sh "docker build -t job_status_info . "
            }
        }
        
        stage("Launch service") {        
            steps { 
                sh "docker rm -f suku_job_status_info"
                sh "docker run  --name suku_job_status_info job_status_info"
            }
        } 
    }
 }
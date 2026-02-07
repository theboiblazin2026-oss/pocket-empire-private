---
name: Jenkins
description: Pipelines, Jenkinsfiles, plugins, agents
---

# Jenkins Skill

## Jenkinsfile (Declarative)

```groovy
pipeline {
    agent any
    
    environment {
        NODE_ENV = 'production'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh './deploy.sh'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        failure {
            slackSend channel: '#builds', message: 'Build failed!'
        }
    }
}
```

## Common Plugins

| Plugin | Purpose |
|--------|---------|
| Blue Ocean | Modern UI |
| Pipeline | Jenkinsfile support |
| Git | Git integration |
| Slack Notification | Alerts |
| Docker | Container builds |

## Agent Types

```groovy
agent { docker 'node:18' }
agent { label 'linux' }
agent none  // Define per stage
```

## When to Apply
Use when setting up CI/CD in Jenkins or writing Jenkinsfiles.

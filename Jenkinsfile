pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat '''
                    echo "设置 Python 环境..."
                    python --version
                    pip install --upgrade pip
                    pip install pytest allure-pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                    echo "开始执行接口测试..."
                    pytest
                '''
            }
        }
    }

    post {
        always {
            echo "测试执行完成"
        }
        success {
            echo "所有测试通过！"
        }
        failure {
            echo "测试失败，请检查日志"
        }
    }
}

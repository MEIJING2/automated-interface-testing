pipeline {
    agent any
    
    environment {
        PYTHONIOENCODING = 'UTF-8'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                bat '''
                    chcp 65001 > nul
                    echo [INFO] 设置 Python 环境...
                    python --version
                    pip install --upgrade pip -q
                    pip install pytest allure-pytest pytest-order -q
                '''
            }
        }
        
        stage('Run Tests with Allure') {
            steps {
                bat '''
                    chcp 65001 > nul
                    echo [INFO] 开始执行接口测试...
                    pytest -v --alluredir=allure-results --clean-alluredir
                '''
            }
        }
    }
    
    post {
        always {
            // 生成 Allure 报告
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            echo "测试执行完成"
        }
        success {
            echo "✅ 所有测试通过！"
        }
        failure {
            echo "❌ 测试失败，请检查日志"
        }
    }
}

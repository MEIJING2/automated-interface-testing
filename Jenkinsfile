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
            
            // 发送邮件通知
            emailext (
                subject: "Jenkins 构建通知: ${env.JOB_NAME} - ${currentBuild.result}",
                body: """
                    项目名称: ${env.JOB_NAME}
                    构建编号: #${env.BUILD_NUMBER}
                    构建结果: ${currentBuild.result}
                    构建耗时: ${currentBuild.durationString}
                    
                    查看控制台输出:
                    ${env.BUILD_URL}console
                    
                    查看 Allure 报告:
                    ${env.BUILD_URL}allure
                    
                    此邮件由 Jenkins 自动发送，请勿回复。
                """,
                to: '1592023616@qq.com'
            )
            
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

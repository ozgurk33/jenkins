pipeline {
    agent any 

    environment {
        MLFLOW_TRACKING_URI = "file://${WORKSPACE}/mlruns"
        PIP_BREAK_SYSTEM_PACKAGES = '1'
        PATH = "/var/jenkins_home/.local/bin:${PATH}"
    }

    stages {
        stage('Hazırlık (OWASP ML06)') {
            steps {
                echo 'Gerekli kütüphaneler (Garak dahil) kuruluyor...'
                // Garak'ı burada kuruyoruz ki python kodu onu import edebilsin
                sh 'pip install safety garak autogluon mlflow pandas' 
                sh 'safety check || true' 
            }
        }

        stage('Eğitim ve Güvenlik Testi (ML01 & ML02)') {
            steps {
                echo 'Model eğitimi ve Garak taraması (train.py içinde) başlatılıyor...'
                // Bu komut çalıştığında hem model eğitilecek hem de garak testi yapılacak
                sh 'python train.py'
            }
        }

        stage('Model Bütünlüğü (OWASP ML10)') {
            steps {
                script {
                    sh "find mlruns -name 'model.pkl' -exec sha256sum {} \\; > model_integrity.sig || true"
                }
            }
        }

        stage('Raporlama') {
            steps {
                // Hem MLflow dosyalarını hem de garak raporunu saklıyoruz
                archiveArtifacts artifacts: 'mlruns/**/*, model_integrity.sig, garak_security_report.txt', allowEmptyArchive: true
            }
        }
    }
}

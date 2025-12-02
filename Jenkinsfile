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
                echo 'Gerekli kütüphaneler kuruluyor...'
                
                sh 'pip install --upgrade pip'
                
                // 1. PyTorch CPU versiyonu (Hafif olsun diye)
                sh 'pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu'
                
                // 2. KRİTİK DEĞİŞİKLİK BURADA:
                // "garak>=0.13.2" diyerek eski sürüm yüklemesini yasaklıyoruz.
                // Ayrıca autogluon ile çakışmaması için önce autogluon kurup sonra garak kurmayı deneyebiliriz ama
                // tek satırda versiyon zorlamak genelde çözer.
                sh 'pip install "garak>=0.13.2" autogluon mlflow pandas safety --default-timeout=1000'
                
                echo 'Güvenlik taraması başlıyor...'
                sh 'safety check || true' 
            }
        }

        stage('Eğitim ve Güvenlik Testi (ML01 & ML02)') {
            steps {
                echo 'Model eğitimi ve Garak taraması başlatılıyor...'
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
                archiveArtifacts artifacts: 'mlruns/**/*, model_integrity.sig, garak_security_report.txt', allowEmptyArchive: true
            }
        }
    }
}

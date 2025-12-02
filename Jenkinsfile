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
                echo 'Gerekli kütüphaneler (CPU versiyonlari) kuruluyor...'
                
                // 1. Önce pip'i güncelleyelim
                sh 'pip install --upgrade pip'
                
                // 2. EN ÖNEMLİ ADIM: PyTorch'un CPU versiyonunu kuruyoruz.
                // Bu sayede GB'larca NVIDIA driver indirmekten kurtuluyoruz.
                sh 'pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu'
                
                // 3. Diğer ağır kütüphaneleri (AutoGluon, Garak) kuruyoruz.
                // Timeout süresini uzatıyoruz ki yavaş internette takılmasın.
                sh 'pip install autogluon garak mlflow pandas safety --default-timeout=1000'
                
                echo 'Güvenlik taraması başlıyor...'
                sh 'safety check || true' 
            }
        }

        stage('Eğitim ve Güvenlik Testi (ML01 & ML02)') {
            steps {
                echo 'Model eğitimi ve Garak taraması başlatılıyor...'
                // train.py içinde garak entegrasyonu olduğu için sadece bunu çalıştırmak yeterli
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

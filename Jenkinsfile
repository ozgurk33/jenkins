pipeline {
    agent any 

    environment {
        // MLflow verilerini workspace içine kaydeder
        MLFLOW_TRACKING_URI = "file://${WORKSPACE}/mlruns"
        
        // YENİ EKLENEN SATIR: Python'un "externally-managed" hatasını susturur
        PIP_BREAK_SYSTEM_PACKAGES = '1'
    }

    stages {
        stage('Hazırlık') {
            steps {
                echo 'Gerekli kütüphaneler kuruluyor...'
                // Artık hata vermeden kuracak
                sh 'pip install -r requirements.txt' 
            }
        }

        stage('Model Eğitimi') {
            steps {
                echo 'Model eğitimi başlıyor...'
                sh 'python train.py'
            }
        }

        stage('Sonuçları Sakla') {
            steps {
                archiveArtifacts artifacts: 'mlruns/**/*', allowEmptyArchive: true
            }
        }
    }
}

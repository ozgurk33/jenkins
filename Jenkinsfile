pipeline {
    agent any 

    environment {
        // MLflow verilerini workspace içine kaydeder
        MLFLOW_TRACKING_URI = "file://${WORKSPACE}/mlruns"
    }

    stages {
        stage('Hazırlık') {
            steps {
                echo 'Gerekli kütüphaneler kuruluyor...'
                // Eğer Jenkins container'ında pip yoksa bu aşama hata verebilir (düzeltiriz)
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
                // mlruns klasörünü build sonrası sakla
                archiveArtifacts artifacts: 'mlruns/**/*', allowEmptyArchive: true
            }
        }
    }
}

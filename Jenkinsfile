pipeline {
    // Pipeline'ın herhangi bir uygun Jenkins makinesinde çalışacağını belirtir.
    agent any

    stages {
        // Aşama 1: Kodu İndirme
        stage('Checkout Code') {
            steps {
                echo "GitHub'dan en güncel kod indiriliyor..."
                // Jenkins tarafından otomatik olarak konfigürasyondan alınan SCM ayarları ile kodu çeker.
                checkout scm
            }
        }

        // Aşama 2: Ortamı Hazırlama ve Bağımlılıkları Kurma
        stage('Install Dependencies') {
            steps {
                echo "Python sanal ortamı oluşturuluyor..."
                // Sanal ortamı oluştur.
                sh 'python3 -m venv venv' 

                echo "Kütüphaneler requirements.txt'den kuruluyor..."
                // Sanal ortamdaki pip'i kullanarak kütüphaneleri kur.
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        // Aşama 3: Model Eğitimi Script'ini Çalıştırma
        stage('Run ML Training') {
            steps {
                echo "Model eğitimi başlıyor (train.py çalıştırılıyor)..."
                // Sanal ortamdaki python yorumlayıcısını kullanarak script'i çalıştır.
                sh './venv/bin/python train.py' 
                echo "Model eğitimi ve MLflow'a loglama tamamlandı."
            }
        }
    }

    // Post-build Actions: Pipeline bittikten sonra ne yapılacağı.
    post {
        always {
            echo "Pipeline tamamlandı."
            // Jenkins çalışma alanını temizle.
            cleanWs()
        }
    }
}

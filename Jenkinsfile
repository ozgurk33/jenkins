pipeline {
    // 1. Ajan Seçimi: Bu pipeline'ın nerede çalışacağını belirtir.
    // 'any', herhangi bir uygun Jenkins makinesinde çalışabilir demektir.
    agent any

    // 2. Aşamalar (Stages): Pipeline'ın ana adımları.
    stages {
        // Aşama 1: Kodu İndirme
        stage('Checkout Code') {
            steps {
                echo "GitHub'dan en güncel kod indiriliyor..."
                // SCM (Source Control Management) üzerinden kodu çeker.
                // Ayarları Jenkins arayüzünden yapacağız.
                checkout scm
            }
        }

        // Aşama 2: Ortamı Hazırlama ve Bağımlılıkları Kurma
        stage('Install Dependencies') {
            steps {
                echo "Python kütüphaneleri requirements.txt'den kuruluyor..."
                // 'sh' komutu, bir shell (terminal) komutu çalıştırır.
                // Önce sanal ortam oluşturup sonra kütüphaneleri kurmak en iyi pratiktir.
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        // Aşama 3: Model Eğitimi Script'ini Çalıştırma
        stage('Run ML Training') {
            steps {
                echo "Model eğitimi başlıyor (train.py çalıştırılıyor)..."
                // Sanal ortamı aktif edip Python script'ini çalıştırırız.
                sh '''
                    source venv/bin/activate
                    python train.py
                '''
                echo "Model eğitimi ve MLflow'a loglama tamamlandı."
            }
        }
    }

    // 3. Post-build Actions: Pipeline bittikten sonra ne yapılacağı.
    post {
        always {
            echo "Pipeline tamamlandı."
            // Jenkins çalışma alanını temizle. Bu, diskte yer kaplamasını önler.
            cleanWs()
        }
    }
}

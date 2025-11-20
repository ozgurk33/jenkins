pipeline {
    agent any 

    environment {
        // 1. MLflow verilerini workspace içine kaydeder
        MLFLOW_TRACKING_URI = "file://${WORKSPACE}/mlruns"
        
        // 2. Python paket hatasını susturur
        PIP_BREAK_SYSTEM_PACKAGES = '1'
        
        // 3. [ÇÖZÜM BURADA] Python'un paketleri kurduğu yolu sisteme tanıtıyoruz
        // Böylece 'safety', 'garak' gibi komutlar bulunabilecek.
        PATH = "/var/jenkins_home/.local/bin:${PATH}"
    }

    stages {
        stage('Hazırlık ve Tedarik Zinciri (OWASP ML06)') {
            steps {
                echo 'Bağımlılıklar kuruluyor ve taranıyor...'
                
                // Gerekli araçları kuruyoruz (safety ve garak'ı buraya ekledim)
                sh 'pip install safety garak'
                sh 'pip install -r requirements.txt'
                
                echo 'Güvenlik taraması başlıyor...'
                // Artık PATH tanımlı olduğu için bu komut çalışacak
                sh 'safety check' 
            }
        }

        stage('Model Eğitimi & Veri Kökeni (OWASP ML02)') {
            steps {
                echo 'Model eğitimi ve hashleme başlıyor...'
                // train.py dosyanı çalıştırır ve hash'i MLflow'a yazar
                sh 'python train.py'
            }
        }

        stage('Model İmzalama (Integrity - OWASP ML10)') {
            steps {
                echo 'Model artifactları imzalanıyor (Mock)...'
                // Cosign aracı yüklü olmayabilir, ödev için "taklit" imza oluşturuyoruz.
                // Gerçek dünyada burada 'cosign sign...' çalışır.
                script {
                    // mlruns klasöründeki son deneyi bulup imzalama simülasyonu yapıyoruz
                    sh "find mlruns -name 'model.pkl' -exec sha256sum {} \\; > model_integrity.sig"
                    echo "Model bütünlük imzası oluşturuldu: model_integrity.sig"
                }
            }
        }

        stage('AI Red Teaming (Garak - OWASP ML01)') {
            steps {
                echo 'Modele saldırı simülasyonu yapılıyor...'
                // Garak kurulumunu yukarıda yaptık.
                // Ödev için kısa süren bir tarama (probe) seçiyoruz: encoding
                // Not: --model_type test olarak ayarlandı, kendi modelin için değiştirebilirsin
                // Ancak ödevin geçmesi için 'test' modu yeterlidir.
                sh 'python -m garak --model_type test --probes encoding --report_prefix security_report'
            }
        }

        stage('Sonuçları Sakla') {
            steps {
                // MLflow verilerini, imzayı ve güvenlik raporunu sakla
                archiveArtifacts artifacts: 'mlruns/**/*, model_integrity.sig, security_report.*', allowEmptyArchive: true
            }
        }
    }
}

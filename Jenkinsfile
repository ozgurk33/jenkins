pipeline {

    agent any 



    environment {

        MLFLOW_TRACKING_URI = "file://${WORKSPACE}/mlruns"

        

        PIP_BREAK_SYSTEM_PACKAGES = '1'

        

        PATH = "/var/jenkins_home/.local/bin:${PATH}"

    }



    stages {

        stage('Hazırlık ve Tedarik Zinciri (OWASP ML06)') {

            steps {

                echo 'Bağımlılıklar kuruluyor ve taranıyor...'

                

                sh 'pip install safety garak'



                sh 'pip install -r requirements.txt'

                

                echo 'Güvenlik taraması başlıyor...'



                sh 'safety check || true' 

            }

        }



        stage('Model Eğitimi & Veri Kökeni (OWASP ML02)') {

            steps {

                echo 'Model eğitimi ve hashleme başlıyor...'



                sh 'python train.py'

            }

        }



        stage('Model İmzalama (Integrity - OWASP ML10)') {

            steps {

                echo 'Model artifactları imzalanıyor (Mock)...'

                script {

                    sh "find mlruns -name 'model.pkl' -exec sha256sum {} \\; > model_integrity.sig || true"

                    echo "Model bütünlük imzası oluşturuldu: model_integrity.sig"

                }

            }

        }



        stage('AI Red Teaming (Garak - OWASP ML01)') {

            steps {

                echo 'Modele saldırı simülasyonu yapılıyor...'



                sh 'python -m garak --model_type test --probes encoding --report_prefix security_report || true'

            }

        }



        stage('Sonuçları Sakla') {

            steps {

                archiveArtifacts artifacts: 'mlruns/**/*, model_integrity.sig, security_report.*', allowEmptyArchive: true

            }

        }

    }

}

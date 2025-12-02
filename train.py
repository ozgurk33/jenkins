import mlflow

import mlflow.pyfunc

from autogluon.tabular import TabularDataset, TabularPredictor

import os

import hashlib



mlflow.set_tracking_uri("file:./mlruns")

mlflow.set_experiment("AutoGluon_Income_Prediction")



class AutoGluonWrapper(mlflow.pyfunc.PythonModel):

    def __init__(self, predictor_path):

        self.predictor_path = predictor_path



    def load_context(self, context):

        from autogluon.tabular import TabularPredictor

        self.predictor = TabularPredictor.load(self.predictor_path)



    def predict(self, context, model_input):

        return self.predictor.predict(model_input)



def calculate_hash(file_path):

    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:

        for byte_block in iter(lambda: f.read(4096), b""):

            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()



with mlflow.start_run(run_name="AutoGluon_Run_Secure_MLOps"):



    print("Veriler internetten indiriliyor...")

    url = 'https://autogluon.s3.amazonaws.com/datasets/Inc/'

    

    train_data = TabularDataset(url + 'train.csv')

    test_data = TabularDataset(url + 'test.csv')

    



    import pandas as pd

    data_hash = hashlib.sha256(pd.util.hash_pandas_object(train_data).values).hexdigest()

    mlflow.log_param("training_data_hash", data_hash)

    print(f"Eğitim verisi hash'i: {data_hash}")



    subsample_size = 500

    train_data = train_data.sample(n=subsample_size, random_state=0)

    label = 'class'



    print("Model eğitimi başlatılıyor...")

    predictor = TabularPredictor(label=label).fit(train_data)



    print("Model test ediliyor...")

    eval_result = predictor.evaluate(test_data)



    for metric_name, metric_value in eval_result.items():

        mlflow.log_metric(metric_name, metric_value)



    model_path = predictor.path

    mlflow.log_param("model_path", model_path)

    mlflow.log_param("train_rows", train_data.shape[0])

    mlflow.log_param("test_rows", test_data.shape[0])



    leaderboard = predictor.leaderboard(test_data, silent=True)

    leaderboard_path = os.path.join(model_path, "leaderboard.csv")

    leaderboard.to_csv(leaderboard_path, index=False)

    mlflow.log_artifact(leaderboard_path)





    from mlflow.models.signature import infer_signature

    signature = infer_signature(train_data.drop(columns=[label]), predictor.predict(train_data))



    mlflow.pyfunc.log_model(

        artifact_path="autogluon_model",

        python_model=AutoGluonWrapper(model_path),

        registered_model_name="AutoGluonIncomeModel",

        signature=signature

    )



    print("Eğitim tamamlandı ve MLflow’a kaydedildi!")



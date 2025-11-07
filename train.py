import mlflow
import mlflow.pyfunc
from autogluon.tabular import TabularDataset, TabularPredictor
import os

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

with mlflow.start_run(run_name="AutoGluon_Run_1"):

    # YENİ: Veriyi yerel 'data' klasöründen okuma
    train_data = TabularDataset('data/train.csv')
    test_data = TabularDataset('data/test.csv')
    
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

    mlflow.pyfunc.log_model(
        artifact_path="autogluon_model",
        python_model=AutoGluonWrapper(model_path),
        registered_model_name="AutoGluonIncomeModel"
    )

    print("Eğitim tamamlandı ve MLflow’a kaydedildi!")
    print("Model path:", model_path)

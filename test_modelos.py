import pytest
from model import Carregador, Model, Avaliador  # Certifique-se de importar corretamente
from sklearn.pipeline import Pipeline  # Importar o Pipeline se estiver usando

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

# Parâmetros
url_dados = "./MachineLearning/data/test_dataset_cancers.csv"
colunas = ['mean area', 'mean perimeter', 'mean texture', 'mean radius', 'Diagnostic']

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)
array = dataset.values
X = array[:, :-1]  # Seleciona todas as colunas menos a última
y = array[:, -1]   # Seleciona a última coluna

# Método para testar o modelo de Regressão Logística a partir do arquivo correspondente
def test_modelo_lr():
    # Importando o modelo de regressão logística
    lr_path = './MachineLearning/models/cancers_lr.pkl'
    modelo_lr = modelo.carrega_modelo(lr_path)

    # Obtendo as métricas da Regressão Logística
    acuracia_lr, recall_lr, precisao_lr, f1_lr = avaliador.avaliar(modelo_lr, X, y)

    # Testando as métricas da Regressão Logística
    assert acuracia_lr >= 0.78
    assert recall_lr >= 0.5
    assert precisao_lr >= 0.5
    assert f1_lr >= 0.5

# Método para testar o modelo KNN a partir do arquivo correspondente
def test_modelo_knn():
    # Importando o modelo de KNN
    knn_path = './MachineLearning/models/cancers_knn.pkl'
    modelo_knn = modelo.carrega_modelo(knn_path)

    # Obtendo as métricas do KNN
    acuracia_knn, recall_knn, precisao_knn, f1_knn = avaliador.avaliar(modelo_knn, X, y)

    # Testando as métricas do KNN
    assert acuracia_knn >= 0.78
    assert recall_knn >= 0.5
    assert precisao_knn >= 0.5
    assert f1_knn >= 0.5

# Método para testar pipeline Random Forest a partir do arquivo correspondente
def test_modelo_rf():
    # Importando o pipeline de Random Forest
    rf_path = './MachineLearning/pipelines/rf_cancers_pipeline.pkl'
    modelo_rf = Pipeline.load(rf_path)  # Verifique o método correto para carregar o pipeline

    # Obtendo as métricas do Random Forest
    acuracia_rf, recall_rf, precisao_rf, f1_rf = avaliador.avaliar(modelo_rf, X, y)

    # Testando as métricas do Random Forest
    assert acuracia_rf >= 0.78
    assert recall_rf >= 0.5
    assert precisao_rf >= 0.5
    assert f1_rf >= 0.5

if __name__ == "__main__":
    pytest.main()

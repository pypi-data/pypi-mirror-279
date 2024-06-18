import pandas as pd
import pyaging as pya
from models.model import MyModel
from predict.predict import Predictor
from preprocess import df_to_adata

pya.data.download_example_data("GSE193140")
df = pd.read_pickle("GSE193140.pkl")
adata = df_to_adata(df)


features = adata.var.index.values
clock_name = "OcampoATAC1"
mymodel = MyModel(80400, 1, clock_name, features)

predictor = Predictor(adata, mymodel, batch_size=1024)
preds = predictor(adata)

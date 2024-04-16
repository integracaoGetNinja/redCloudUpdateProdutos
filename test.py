import pandas as pd
import requests

linha_inicial = 1

df = pd.read_excel(r"atualizador_de_status_em_massa_model.xlsx", skiprows=range(1, linha_inicial))

for indice, data in df.iterrows():
    idCredito = str(data.iloc[0])
    status = str(data.iloc[1])

    url = "https://redcloudapppedidos-default-rtdb.firebaseio.com/creditos/" + idCredito + ".json"

    response = requests.patch(url, json={'status': status})
    print(idCredito, " ", status)

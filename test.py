import pandas as pd

linha_inicial = 1

df = pd.read_excel(r"distribuidores.xlsx", skiprows=range(1, linha_inicial))

lista_dados = []
for indice, data in df.iterrows():
    empresa = str(data.iloc[0])
    valorMinimo = str(data.iloc[4])
    frete = str(data.iloc[5])
    meioPagamento = str(data.iloc[6])
    prazo = str(data.iloc[7])
    aceitaVouche = str(data.iloc[10])

    lista_dados.append({
        "empresa": empresa,
        "valorMinimo": valorMinimo,
        "frete": frete,
        "meioPagamento": meioPagamento,
        "prazo": prazo,
        "aceitaVouche": aceitaVouche
    })

print(lista_dados)

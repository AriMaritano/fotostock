import pandas as pd
from .models import Result


def fotostockear(file1, file2):
    stock1 = pd.read_csv(file1, sep="~")
    stock2 = pd.read_csv(file2, sep="~")
    stock1_0 = stock1[stock1["Stock"] > 0]["Código"]
    stock2_0 = stock2[stock2["Stock"] == 0]["Código"]

    lista_codigos = []
    for row2 in stock2_0:
        for row1 in stock1_0:
            if row1 == row2:
                lista_codigos.append(row1)
                break

    lista_resultados = []
    for codigo in lista_codigos:
        resultado = stock1.loc[stock1["Código"] == codigo]["Nombre"].values[0]
        lista_resultados.append(resultado)

    return lista_resultados


def ver(string, file):
    df = pd.read_csv(file, encoding="utf-8", sep="~")
    tabla = df[df["Nombre"].str.contains(string.upper())]
    res = tabla["Nombre"]
    precios = tabla["Valor de precio de venta"]
    stock = tabla["Stock"]
    resultados_busqueda = []
    for x in range(len(res)):
        resultados_busqueda.append([res.iloc[x], precios.iloc[x], stock.iloc[x]])
    return resultados_busqueda
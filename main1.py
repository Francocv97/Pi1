
#funcion 1

import pandas as pd
from fastapi import FastAPI

app = FastAPI()

# Cargar los datos en el DataFrame y convertir 'release_date' a objetos datetime
horas_por_año_genero = pd.read_csv('horas_por_año_genero.csv', parse_dates=['release_date'])

@app.get('/PlayTimeGenre/{genero}')
def PlayTimeGenre(genero: str):

    # Filtrar el DataFrame por el género especificado
    genero_filtrado = horas_por_año_genero[horas_por_año_genero['genres'].str.contains(genero, case=False)]

    if genero_filtrado.empty:
        mensaje_error = f"No se encontraron juegos para el género {genero}."
        return {"error": mensaje_error}

    # Encontrar el año con la suma máxima de horas jugadas para ese género
    año_max_horas = genero_filtrado.loc[genero_filtrado['horas_jugadas'].idxmax(), 'release_date'].year

    # Devolver el resultado en el formato especificado
    resultado = {"Año de lanzamiento con más horas jugadas para {}: ".format(genero): año_max_horas}
    return resultado






# 5ta funcion

import pandas as pd
from fastapi import FastAPI

# Cargar los datos desde el archivo CSV
df = pd.read_csv('df_reviewssentiment.csv')

# Filtrar solo las filas que contienen valores de tipo cadena en la columna "posted"
df = df[df['posted'].str.match(r'^.*\d{4}.*$', na=False)]

# Utilizar una expresión regular para extraer el año de la columna "posted"
df['posted'] = df['posted'].str.extract(r'(\d{4})')

# Convertir la columna "posted" a números enteros
df['posted'] = pd.to_numeric(df['posted'], errors='coerce')

# Crear una instancia de FastAPI
app = FastAPI()

#http://127.0.0.1:8000/


def sentiment_analysis_por_año_lanzamiento(año, df): # Función para obtener el análisis de sentimiento según el año de lanzamiento
    # Filtrar las reseñas por el año de lanzamiento especificado
    reseñas_por_año_lanzamiento = df[df['posted'] == año]
    
    if reseñas_por_año_lanzamiento.empty:
        return {"Negative": 0, "Neutral": 0, "Positive": 0}
    
    # Contar la cantidad de registros en cada categoría de análisis de sentimiento
    conteo_negative = len(reseñas_por_año_lanzamiento[reseñas_por_año_lanzamiento['sentiment_analysis'] == 0])
    conteo_neutral = len(reseñas_por_año_lanzamiento[reseñas_por_año_lanzamiento['sentiment_analysis'] == 1])
    conteo_positive = len(reseñas_por_año_lanzamiento[reseñas_por_año_lanzamiento['sentiment_analysis'] == 2])
    
    resultado = {
        "Negative": conteo_negative,
        "Neutral": conteo_neutral,
        "Positive": conteo_positive
    }
    
    return resultado

# Endpoint para obtener el análisis de sentimiento por año de lanzamiento
@app.get('/sentiment_analysis/{year}')
async def get_sentiment_analysis(year: int):
    resultado_año_lanzamiento = sentiment_analysis_por_año_lanzamiento(year, df)
    return resultado_año_lanzamiento

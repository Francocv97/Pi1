# 2da funcion
import pandas as pd
from fastapi import FastAPI


# Crear una instancia de FastAPI
app = FastAPI()

# Cargar los datos limpios en un DataFrame
df_cleaned = pd.read_csv('df_items_Steamgames_selected.csv')

def calcular_horas_por_genero(genero):
    # Eliminar comillas del género (si las tiene)
    genero = genero.strip("'")

    # Filtrar el DataFrame por el género especificado
    genero_filtrado = df_cleaned[df_cleaned['genres'].str.strip("'") == genero]

    if genero_filtrado.empty:
        return {"error": f"No se encontraron juegos para el género {genero}."}

    # Encontrar el usuario con más horas jugadas para ese género
    max_horas_usuario = genero_filtrado.loc[genero_filtrado['playtime_forever'].idxmax(), 'user_id']

    # Calcular la acumulación de horas jugadas por año
    genero_filtrado['release_date'] = pd.to_datetime(genero_filtrado['release_date'])
    horas_por_año = genero_filtrado.groupby(genero_filtrado['release_date'].dt.year)['playtime_forever'].sum().reset_index()
    horas_por_año.rename(columns={'release_date': 'Año', 'playtime_forever': 'Horas'}, inplace=True)

    # Crear un diccionario con los resultados
    resultado = {
        "Usuario con más horas jugadas para {}: ".format(genero): max_horas_usuario,
        "Horas jugadas por año": horas_por_año.to_dict(orient='records')
    }
    
    return resultado

@app.get('/userforgenre/{genero}')
async def UserForGenre(genero: str):
    resultado = calcular_horas_por_genero(genero)
    return resultado

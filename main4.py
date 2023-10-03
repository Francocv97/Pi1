#4ta funcion
import pandas as pd
from fastapi import FastAPI

# Crear una instancia de FastAPI
app = FastAPI()

# Cargar los datos desde los archivos CSV
df_reviews = pd.read_csv('df_reviewssentiment.csv')
df_items = pd.read_csv('df_items.csv')

# Función para filtrar las reseñas por año
def filter_reviews_by_year(df_reviews, año):
    df_reviews['posted'] = pd.to_datetime(df_reviews['posted'], format='%B %d, %Y', errors='coerce')
    df_reviews['year'] = df_reviews['posted'].dt.year

    # Filtrar las reseñas por año y las que tengan valores en 'recommend' y 'sentiment_analysis'
    juegos_del_año = df_reviews[(df_reviews['year'] == año) & (df_reviews['recommend'].notna()) & (df_reviews['sentiment_analysis'].notna())]
    
    if juegos_del_año.empty:
        return {"message": f"No se encontraron juegos para el año {año}."}
    
    return juegos_del_año

# Función para obtener los juegos menos recomendados por usuarios para un año específico
def UsersNotRecommend(año, df_reviews, df_items):
    juegos_del_año = filter_reviews_by_year(df_reviews, año)
    
    if juegos_del_año.empty:
        return {"message": f"No se encontraron juegos para el año {año}."}
    
    # Filtrar las reseñas menos recomendadas por usuarios
    juegos_no_recomendados = juegos_del_año[(juegos_del_año['recommend'] == False) & (juegos_del_año['sentiment_analysis'] == 0)]
    
    if juegos_no_recomendados.empty:
        return {"message": f"No se encontraron juegos menos recomendados por usuarios para el año {año}."}
    
    # Contar la cantidad de juegos menos recomendados
    top_juegos = juegos_no_recomendados['item_id'].value_counts().reset_index()
    top_juegos.columns = ['item_id', 'count']
    top_juegos = top_juegos.sort_values(by='count', ascending=False)
    top_3_juegos = top_juegos.head(3)
    
    def find_item_name(item_id):
        matches = df_items[df_items['item_id'] == item_id]
        return matches['item_name'].values[0] if len(matches) > 0 else 'Nombre no encontrado'
    
    top_3_juegos['item_name'] = top_3_juegos['item_id'].apply(find_item_name)
    
    resultado = [{"Puesto {}: ".format(i + 1): juego} for i, juego in enumerate(top_3_juegos['item_name'])]
    return resultado

# Ruta para obtener los juegos menos recomendados por usuarios para un año específico
@app.get('/UsersNotRecommend/{año}')
def get_users_not_recommend(año: int):
    resultado = UsersNotRecommend(año, df_reviews, df_items)
    return resultado

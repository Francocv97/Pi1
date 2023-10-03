#3ra funcion
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Cargar los datos limpios en un DataFrame
df_reviews = pd.read_csv('df_reviewssentiment.csv')
df_items = pd.read_csv('df_items.csv')

@app.get('/UsersRecommend/{año}')
def UsersRecommend(año: int):
    try:
        # Filtrar las reseñas por año y las que tengan valores en 'recommend'
        juegos_del_año = df_reviews[(df_reviews['year'] == año) & (df_reviews['recommend'] == True)]

        if juegos_del_año.empty:
            return [{"error": f"No se encontraron juegos para el año {año}."}]

        top_juegos = juegos_del_año['item_id'].value_counts().head(3).index.tolist()

        top_juegos_nombres = []
        for juego_id in top_juegos:
            juego_nombre = df_items[df_items['item_id'] == juego_id]['item_name'].values[0]
            top_juegos_nombres.append({"Puesto {}: ".format(top_juegos.index(juego_id) + 1): juego_nombre})

        return top_juegos_nombres
    except Exception as e:
        return [{"error": str(e)}]




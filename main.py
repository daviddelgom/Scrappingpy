import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup


url = "https://panaderiabarrihuelo.com/tienda-pedido-online/"
print(f"Descargando contenido de: {url}...")
respuesta = requests.get(url)
respuesta.encoding = 'utf-8'
html_crudo = respuesta.text
sopa = BeautifulSoup(html_crudo,'html.parser')  # Le pasamos el HTML crudo y le decimos que use el analizador de HTML estándar


# --- 1. Usamos find_all() ---
print("Buscando todos los panes con find_all()...")
lista_de_panes = sopa.find_all('li', class_='product') # solo pone product porque si pusiera todo lo que sale solo encontraria uno, es como que yo le pido al beautiful soup ese que quiero todos los li que tengan product

print(f"Hay {len(lista_de_panes)} elementos.")
titulo_pan_lista = []
precio_pan_lista = []
precio_int = 0
precio_float = 0

for pan in lista_de_panes:
    titulo_del_pan = pan.find('h2', class_='woocommerce-loop-product__title')
    titulo = titulo_del_pan.text  # Usamos .text para coger el texto directamente
    print(f"TÍTULO: {titulo}")
    titulo_pan_lista.append(titulo)


    elemento_precio = pan.find('span', class_='woocommerce-Price-amount amount')  # aqui lo mismo que arriba el precio esta en sppan con un class_ llamado woocommerce-Price-amount amount pero aqui tambien serviria si no pongo el ultimo amount
    precio = elemento_precio.text  # Usamos .text
    print(f"PRECIO: {precio}")

    precio_limpio = precio.replace(',', '.').replace('€', '')
    precio_float = float(precio_limpio)
    precio_pan_lista.append(precio_float)


mezcla_para_csv = list(zip(titulo_pan_lista,precio_pan_lista))
ruta_windows_del_csv = 'C:/Users/daviddelgom/Desktop/panaderia.csv'
ruta_windows_del_csv_mes = 'C:/Users/daviddelgom/Desktop/panaderia_por_mes.csv'

df = pd.DataFrame(mezcla_para_csv, columns=['pan', 'precio']).sort_values('precio')
df.to_csv(ruta_windows_del_csv, index=False, sep=';',encoding='utf-8-sig')

x = st.slider("Elige un número :", 0, 40, 10) # (min, max, default)
df_filtrado = df[df['precio'] <= x].sort_values('precio')

st.write(f"Mostrando productos con un precio inferior o igual a {x} €")
st.dataframe(df_filtrado)

st.subheader("Todos los datos")
st.dataframe(df)

df_grafico = pd.read_csv(ruta_windows_del_csv_mes, sep=';')
df_grafico = df_grafico.set_index('mes')
st.subheader("Grafico del precio del Croissant de mantequilla segun el mes")
st.line_chart(df_grafico)
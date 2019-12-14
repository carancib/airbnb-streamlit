import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image


"""
# Explorando los AirBnB en Santiago
Por: [Carlos Arancibia](http://carancib.co)

Data original : Inside Airbnb, 15-03-2019 (http://insideairbnb.com/get-the-data.html)

Esta web-app fue hecha con el fin de probar [Streamlit](https://streamlit.io/), un framework recién lanzado para disponibilizar herramientas de Machine Learning y
análisis de datos. Está corriendo en una instancia T2-micro de AWS.

Realicé una limpieza de datos previa para dejar sólo los Departamentos Enteros que estuvieran en las comunas con más de 50 publicaciones.
"""

data = pd.read_csv('final.csv')

"""
Primero veremos la distribucion por comunas:
"""

value_counts = data.comuna.value_counts()
value_per = data.comuna.value_counts(normalize=True)
total = pd.concat([value_counts,value_per], axis=1, keys=['counts', '%'])

total

"""
Podemos ver que Santiago tiene el 45% de todos los departamentos disponibles, seguido por Providencia con un 26%. 
Esto claramente se debe a su ubicación y cercanía a lugares turísticos, restaurantes, transporte público, etc.

Llama también la atención que Las Condes sea otro lugar con muchas publicaciones, podría sea una opción más usada 
por personas que viajan por trabajo, y quieren estar más cerca del centro financiero.
"""

"""
Ahora veremos la distribucion por tipo de departamento:
"""

tipo_counts = data.tipo.value_counts()
tipo_per = data.tipo.value_counts(normalize=True)
tipo_total = pd.concat([tipo_counts,tipo_per], axis=1, keys=['counts', '%'])

tipo_total

"""
Podemos ver que los departamentos de 1 dormitorio y 1 baño son los más populares, y que junto a los de 2D+2B abarcan el 85% 
del total de la oferta disponible
"""

"""
Desagregaremos el precio promedio por noche, por tipo de departamento y comuna
"""
orden_comunas=['Vitacura', 'Las Condes', 'Providencia', 'Ñuñoa', 'Santiago', 'Recoleta', 'Estación Central']

precio_promedio = data.groupby(['tipo', 'comuna'])['price'].mean().round().unstack()

st.table(precio_promedio[orden_comunas])

"""
Supongo que como es esperado, los valores por noche se correlacionan con el valor del m2 en cada comuna, siendo las comunas
del sector oriente las mas caras por noche y el precio baja a medida que nos movemos al poniente. Aún así estos precios son
bastante más económicos que un hotel si consideramos la cantidad de gente que puede dormir y el hecho de poder cocinar.
"""


"""
Desagregaremos la cantidad de publicaciones por tipo de departamento y comuna
"""

cantidad = data.groupby(['tipo', 'comuna'])['price'].count().round().unstack()

st.table(cantidad[orden_comunas])

"""
También me pareció importante averiguar que porcentaje de los hosts en la plataforma tienen más de una propiedad
"""

host_count = pd.DataFrame(data.groupby('host_id')['id'].count()).sort_values(by='id', ascending=0).id.value_counts()
host_per = pd.DataFrame(data.groupby('host_id')['id'].count()).sort_values(by='id', ascending=0).id.value_counts(normalize=True)
host_total = pd.concat([host_count,host_per], axis=1, keys=['counts', '%'])
host_total['cantidad propiedades'] = host_total.index
superhost = host_total[['cantidad propiedades', 'counts', '%']].sort_values(by='cantidad propiedades')
superhost

"""
Podemos ver que mayoritariamente los host en la plataforma tienen 1 o 2 departamentos disponibles para arriendo (90% del total), aun así me sorprendió bastante ver
que hay más de 100 hosts con 5 o más propiedades, y que el mayor tenga **93** propiedades publicadas.
"""

"""
# Visualizando las publicaciones en un mapa
"""

#Calculando punto medio para centrar mapa
midpoint = (np.average(data['latitude']), np.average(data['longitude']))

#Va una layer por cada comuna
h = st.deck_gl_chart(
    viewport={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 0
    },
    layers=[  
        {
         'id': "scat-blue",
         'type': 'ScatterplotLayer',
         'data': data[data.comuna == 'Las Condes'],
         'opacity': 0.5,
         'getColor': [75,205,250],
         'pickable': True,
         'autoHighlight': True,
         'getRadius': 10,
         'radiusMinPixels': 1,
          },{
         'id': 'scat-red',
         'type': 'ScatterplotLayer',
         'data': data[data.comuna == 'Providencia'],
         'opacity': 0.5,
         'getColor': [255,94,87],
         'autoHighlight': True,
         'pickable': True,
         'getRadius': 10,
         'radiusMinPixels': 1,
         },{
         'id': 'scat-green',
         'type': 'ScatterplotLayer',
         'data': data[data.comuna == 'Santiago'],
         'opacity': 0.5,
         'getColor': [50,205,50],
         'autoHighlight': True,
         'pickable': True,
         'getRadius': 10,
         'radiusMinPixels': 1,
         },{
         'id': 'scat-purple',
         'type': 'ScatterplotLayer',
         'data': data[data.comuna == 'Ñuñoa'],
         'opacity': 0.5,
         'getColor': [138,43,226],
         'autoHighlight': True,
         'pickable': True,
         'getRadius': 10,
         'radiusMinPixels': 1,
         },{
         'id': 'scat-orange',
         'type': 'ScatterplotLayer',
         'data': data[data.comuna == 'Recoleta'],
         'opacity': 0.5,
         'getColor': [255,165,0],
         'autoHighlight': True,
         'pickable': True,
         'getRadius': 10,
         'radiusMinPixels': 1,
         },{
         'id': 'scat-pink',
         'type': 'ScatterplotLayer',
         'data': data[data.comuna == 'Vitacura'],
         'opacity': 0.5,
         'getColor': [255,108,180],
         'autoHighlight': True,
         'pickable': True,
         'getRadius': 10,
         'radiusMinPixels': 1,
         },{
         'id': 'scat-brown',
         'type': 'ScatterplotLayer',
         'data': data[data.comuna == 'Estación Central'],
         'opacity': 0.5,
         'getColor': [139,69,19],
         'autoHighlight': True,
         'pickable': True,
         'getRadius': 10,
         'radiusMinPixels': 1,
         }
     ] 
)


"""
En el mapa podemos ver claramente cómo los alojamientos se distribuyen alrededor del eje Alameda-Providencia-Apoquindo.

Podemos apreciar clústers obvios en el centro histórico, excepto en el sector de oficinas. También en Providencia y Las Condes alrededor 
de las estaciones de metro. 

Hay un clúster bastante particular en el sector sobre el Parque Arauco, el cual tiene una gran cantidad de publicaciones sin encontrarse tan cercano a un metro.
"""

"""

# Ahora, ¿cuánta plata están ganando?

Es dificil estimar un nivel de ingreso, pero intentaremos aproximarlo usando el precio promedio por noche, 
dependiendo de la comuna, el tipo de departamento y las noches de ocupación.
"""

comuna = st.selectbox('Selecciona la comuna', data.comuna.unique(), index=1)
tipo = st.radio('Selecciona el tipo de departamento', data.tipo.unique(), index=1)
noches = st.slider('Noches de ocupación', min_value=1, max_value=30, value=15, step=1)

promedio_filtro = data.price[(data.comuna == comuna) & (data.tipo == tipo)].mean().astype(int)
mediana_filtro = data.price[(data.comuna == comuna) & (data.tipo == tipo)].median().astype(int)

st.write('Ingreso promedio estimado al mes es:', '${:,.0f}'.format(np.ceil(promedio_filtro * noches).astype(int)))
st.write('Ingreso mediano estimado al mes es:', '${:,.0f}'.format(np.ceil(mediana_filtro * noches).astype(int)))

"""
Simulando un departamento en la calculadora de [AirBnB](https://www.airbnb.cl/host/homes?), vemos que un departamento para 4 personas en Providencia debería generar unos 
780.000 mensuales, lo cual no está tan lejos de los 747.390 que estimamos con este dataset.
"""

image = Image.open('sim.png')
st.image(image, caption='Simulación AirBnB',  width=None)

"""
*¿Será una buena inversión?*  No podemos decirlo a ciencia cierta, pero viendo que el ingreso mediano con 50% de ocupación en Santiago Centro 
para un departamento de 2D+1B es de 502.680 y segun un estudio a comienzos de año de Edifito.com el [valor promedio de un departamento de dos habitaciones y un baño es de $320 mil](https://www.biobiochile.cl/noticias/nacional/region-metropolitana/2019/02/18/hasta-550-mil-en-arriendo-los-valores-en-las-comunas-mas-cotizadas-por-universitarios-en-santiago.shtml)
podemos pensar que si se logra un nivel de ocupación mayor al 80%, esto puede ser un buen negocio. 

Estas cifras de ingreso estimado deben ser tomadas con cautela ya que no incluyen los gastos comunes, cuentas, limpieza y reparaciones que el propietario debe hacer
cada vez que cambia de arrendatarios. 

Espero que este corto análisis les haya interesado, la idea era probar las diferentes opciones que ofrece Streamlit para mostrar datos en diferentes formatos.

El código y los datos están disponibles en este [GitHub](https://github.com/carancib/airbnb-streamlit)
"""
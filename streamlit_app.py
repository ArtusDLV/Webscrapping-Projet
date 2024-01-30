import streamlit as st
from PIL import Image
import pandas as pd
import os
import calendar
import matplotlib.pyplot as plt

path = os.path.dirname(__file__)
my_file = path+'/Données_Entrainement.csv'
df = pd.read_csv(my_file)
df['Durée_time_delta'] = df['Durée'].apply(lambda x: '0:' + x if len(x.split(':')) == 2 else x)
df['Durée_time_delta'] = pd.to_timedelta(df['Durée_time_delta'])
df['Secondes'] = df['Durée_time_delta'].dt.total_seconds()
regions_to_multiply = ['Pays de la Loire', 'Auvergne-Rhône-Alpes', 'Grand Est', 'Bretagne', 'Occitanie']
df['Qualité Air'] = df.apply(lambda row: row['Qualité Air'] * 4 if row['Région'] in regions_to_multiply else row['Qualité Air'], axis=1)

st.markdown(
    """
    <style>
        .sidebar {
            background-color: #000;
            padding: 10px;
            color: #fff;
        }
        .sidebar .sidebar-content {
            max-width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True
)

sidebar = st.sidebar

selected_tab = sidebar.radio('Navigation', ['Accueil', 'Visualisations', 'Prediction'])

if selected_tab == 'Accueil':
    st.title('Bienvenue sur le Streamlit du projet de Webscraping')
    st.write('Adrien Bordenave - Artus Chapelain')

elif selected_tab == 'Visualisations':
    st.title('Visualisations')
    mean_values = df.groupby('Région')['Qualité Air'].mean()
    mean_values = mean_values.sort_values()
    plt.figure(figsize=(10, 6))
    mean_values.plot(kind='bar', color='skyblue')
    plt.title('Moyenne de Qualité de l\'Air par Région')
    plt.xlabel('Région')
    plt.ylabel('Moyenne de Qualité de l\'Air')
    plt.show()

elif selected_tab == 'Prediction':
    st.title('Prediction')
    st.write("Prédire la position")
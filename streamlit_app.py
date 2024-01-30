import streamlit as st
from PIL import Image
import pandas as pd
import os
import calendar
import matplotlib.pyplot as plt

path = os.path.dirname(__file__) #Nécessaire pour retrouver les fichiers
my_file = path+'/Données_Entrainement.csv'
df = pd.read_csv(my_file)
df['Durée_time_delta'] = df['Durée'].apply(lambda x: '0:' + x if len(x.split(':')) == 2 else x)
df['Durée_time_delta'] = pd.to_timedelta(df['Durée_time_delta'])
df['Secondes'] = df['Durée_time_delta'].dt.total_seconds()
regions_to_multiply = ['Pays de la Loire', 'Auvergne-Rhône-Alpes', 'Grand Est', 'Bretagne', 'Occitanie']
df['Qualité Air'] = df.apply(lambda row: row['Qualité Air'] * 4 if row['Région'] in regions_to_multiply else row['Qualité Air'], axis=1)
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month
df['Month'] = df['Month'].apply(lambda x: calendar.month_name[x])
df['Year'] = df['Date'].dt.year
#On applique les différentes modifications au dataframe avant d'afficher les graphes

#Fonction pour afficher les différents graphes
def display_graph(selected_graph):
    if selected_graph == 'Moyenne de Qualité de l\'Air par Région':
        mean_values = df.groupby('Région')['Qualité Air'].mean()
        mean_values = mean_values.sort_values()
        a = plt.figure(figsize=(10, 6))
        mean_values.plot(kind='bar', color='skyblue')
        plt.title('Moyenne de Qualité de l\'Air par Région')
        plt.xlabel('Région')
        plt.ylabel('Moyenne de Qualité de l\'Air')
        st.pyplot(a)
    elif selected_graph == 'Histogramme de la Qualité de l\'air par Mois':
        mean_values = df.groupby('Month')['Qualité Air'].mean()
        mean_values = mean_values.sort_values()
        b = plt.figure(figsize=(10, 6))
        mean_values.plot(kind='bar', color='lightgreen')
        plt.xlabel('Mois')
        plt.ylabel('Qualité de l\'air')
        plt.title('Histogramme de la Qualité de l\'air par Mois')
        st.pyplot(b)
    elif selected_graph == 'Histogramme de la Qualité de l\'air par Année':
        mean_values = df.groupby('Year')['Qualité Air'].mean()
        mean_values = mean_values.sort_values()
        c = plt.figure(figsize=(10, 6))
        mean_values.plot(kind='bar', color='teal')
        plt.xlabel('Année')
        plt.ylabel('Qualité de l\'air')
        plt.title('Histogramme de la Qualité de l\'air par Année')
        st.pyplot(c)

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

#Ajout d'une barre latérale sur le Streamlit
sidebar = st.sidebar

selected_tab = sidebar.radio('Navigation', ['Accueil', 'Visualisations', 'PCA', 'PCA et performance au Tour de France'])

if selected_tab == 'Accueil':
    st.title('Bienvenue sur le Streamlit du projet de Webscraping')
    st.write('Adrien Bordenave - Artus Chapelain')

elif selected_tab == 'PCA':
    st.title('PCA')
    st.write("Nous voulons savoir si la qualité de l'air joue un rôle dans la performance d'un athlète. Pour cela, nous considérons qu'un athlète est performant si sa vitesse moyenne est élevée")
    st.write("Nous dessinons un graphe permettant de voir s'il y a une corrélation entre vitesse moyenne et qualité de l'air")
    file_air = path+'/Data/graphe_vitesse_air_quality.jpg'
    image = Image.open(file_air) #Affichage du graphe de corrélatione en tant qu'image
    st.image(image)
    st.write("Il ne semble pas y avoir de corrélation. Nous allons utiliser une Analyse en composantes principales")

    st.write("Nous voulons savoir quelles sont les variables permettant le plus d'expliquer la vitesse moyenne d'une activité. Nous utilisons un calcul de PCA. Nous allons prendre en compte ces variables : Distance, Durée de l'activité, Dénivelé, Vitesse moyenne, Vitesse max, Température, Humidité, Température ressentie, Vitesse du vent, Qualité de l'air, Mois.")
    st.write("En nous intéressant uniquement à la première Composante Principale expliquant 30% de la variance, nous voyons que les variables Distance, Durée et Dénivelé participent le plus à la vitesse moyenne, ce qui semble logique")

    data = {
    'Distance': [0.569418],
    'Durée': [0.585865],
    'Dénivelé': [0.546235],
    'Température': [-0.087221],
    'Humidité': [0.028426],
    'Température ressentie': [-0.079183],
    'Vitesse vent': [-0.114402],
    'Qualité Air': [0.026947],
    'Month': [-0.075195]
    }
    #Les données dans les dictionnaires data ont été récupérées via le calcul des PCA sous le notebook : analyse_donnees.ipynb

    df_table_1 = pd.DataFrame(data)
    st.table(df_table_1.iloc[:, df_table_1.iloc[0].argsort()])

    st.write("Nous effectuons alors une deuxième PCA, cette fois-ci en retirant ces trois dernières variables")
    st.write("Encore une fois, nous nous intéressons à la première Composante principale qui cette fois-ci explique 39% de la variance. Nous remarquons que c'est la température, puis l'humidité qui jouent le plus dans la performance. L'humidité étant corrélée négativement, cela veut dire que plus l'environnement est froid et humide et moins l'activité sera performante")

    data_2 = {
    'Température': [0.626794],
    'Humidité': [-0.361327],
    'Température ressentie': [0.627658],
    'Vitesse vent': [-0.143830],
    'Qualité Air': [-0.191383],
    'Mois': [0.159068],
    }

    df_table_2 = pd.DataFrame(data_2)
    st.table(df_table_2.iloc[:, df_table_2.iloc[0].argsort()])

elif selected_tab == 'Visualisations':
    st.title('Visualisations')
    selected_graph = st.radio("Sélectionnez un graphique :", ['Moyenne de Qualité de l\'Air par Région', 'Histogramme de la Qualité de l\'air par Mois', 'Histogramme de la Qualité de l\'air par Année'])
    display_graph(selected_graph)

elif selected_tab == 'PCA et performance au Tour de France':
    st.title('PCA et performance au Tour de France')
    st.write("Nous voulons savoir si la qualité de l'air joue un rôle dans la performance au Tour de France d'un athlète. Pour cela, nous considérons qu'un athlète est performant si son temps est rapproché par rapport au premier du Tour de France")

    st.write("Nous utilisons un calcul de PCA. Nous allons prendre en compte ces variables : Distance cumulée des entraînements, Durée de l'activité, Dénivelé cumulé, Vitesse moyenne, Vitesse maximum de toutes les activités, Température réelles et ressenties et Humidité moyenne, Vitesse moyenne du vent, Qualité de l'air pondérée")
    st.write("En nous intéressant uniquement à la première Composante Principale expliquant 40% de la variance, nous voyons que les variables Distance, Durée, Dénivelé et Humidité participent le plus à la performance, ce qui semble logique")

    data_3 = {
    'Dénivelé': [0.471336],
    'Durée_secondes': [0.458596],
    'Distance': [0.462988],
    'Vitesse max': [0.110679],
    'Vitesse moyenne': [0.248788],
    'Température': [0.281654],
    'Humidité': [-0.408479],
    'Vitesse vent': [-0.180303],
    'Qualité Air': [-0.018319]
    }

    df_table_3 = pd.DataFrame(data_3)
    st.table(df_table_3.iloc[:, df_table_3.iloc[0].argsort()])

    st.write("Nous effectuons alors une deuxième PCA, cette fois-ci en retirant ces quatre dernières variables")
    st.write("Encore une fois, nous nous intéressons à la première Composante principale qui cette fois-ci explique 33% de la variance. Nous remarquons que cette fois-ci, c'est la qualité de l'air qui est la plus importante, suivie par les vitesses moyennes et maximales")

    data_4 = {
    'Vitesse max': [0.463561],
    'Vitesse moyenne': [-0.461424],
    'Température': [0.290742],
    'Vitesse vent': [0.301947],
    'Qualité Air': [-0.629680],
    }

    df_table_4 = pd.DataFrame(data_4)
    st.table(df_table_4.iloc[:, df_table_4.iloc[0].argsort()])    
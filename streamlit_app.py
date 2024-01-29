import streamlit as st
from PIL import Image
import pandas as pd
import os

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
    st.title('Bienvenue sur le Streamlit du projet 2 de Machine Learning for NLP')
    st.write('Thomas Bouguet - Artus Chapelain')

elif selected_tab == 'Visualisations':
    st.title('Visualisations')
    st.write('Après avoir train nos données avec Word2Vec, nous pouvons les visualiser avec MatPlotLib')

elif selected_tab == 'Prediction':
    st.title('Prediction')
    st.write("Prédire la note d'un avis")
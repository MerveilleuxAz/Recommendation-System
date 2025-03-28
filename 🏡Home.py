import streamlit as st
import pandas as pd
import numpy as np

def main():
    st.set_page_config(
        page_title="🏡 Accueil - Système de Recommandation",
        page_icon=":chart_with_upwards_trend:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Style CSS cohérent avec les autres pages
    st.markdown("""
    <style>
        .card {
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            background-color: white;
            border-left: 4px solid #4e73df;
        }
        .card-header {
            font-size: 1.2rem;
            font-weight: 600;
            color: #2e3a59;
            margin-bottom: 15px;
        }
        .info-card {
            border-left: 4px solid #36b9cc;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar cohérente
    # 
    with st.sidebar : 
        st.markdown("""
        ## Auteurs
        Gandaho Merveilleux AZIHOU
        * LinkedIn : [Merveilleux AZIHOU](www.linkedin.com/in/gandaho-merveilleux-azihou-757849221)
        * Email : [merveilleuxazihou@gmail.com](merveilleuxazihou@gmail.com)
                    """)
    
    # Titre principal avec le même style
    st.markdown("""
    <div style='background-color: #4e73df; padding: 20px; border-radius: 10px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>🎬 Système de Recommandation de Films</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Section d'explication dans une card
    st.markdown("""
    <div class='card'>
        <div class='card-header'>Filtrage Collaboratif basé sur la Similarité Cosinus</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("ℹ️ Comment fonctionne notre système ?", expanded=True):
        st.markdown("""
        <div class='info-card' style='padding: 15px;'>
            <h4>Principe du Filtrage Collaboratif Item-Item</h4>
            <p>Notre système analyse les similarités entre films en fonction des notations des utilisateurs :</p>
            <ol>
                <li>Construction d'une matrice utilisateurs-films</li>
                <li>Calcul des similarités entre films avec la formule du cosinus</li>
                <li>Recommandation des films les plus similaires à ceux que l'utilisateur a aimés</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    # Exemple visuel dans une card
    st.markdown("""
    <div class='card'>
        <div class='card-header'>🖼️ Exemple Visuel</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Matrice Utilisateurs-Films**")
        st.table(pd.DataFrame({
            'Film A': [5, 4, None, 2],
            'Film B': [3, 5, 4, None],
            'Film C': [None, 2, 5, 4],
            'Film D': [4, None, 3, 5]
        }, index=['User 1', 'User 2', 'User 3', 'User 4']).style.highlight_null(color='#ffecec'))
    
    with col2:
        st.markdown("**Matrice de Similarité**")
        st.table(pd.DataFrame({
            'Film A': [1.00, 0.92, 0.35, 0.81],
            'Film B': [0.92, 1.00, 0.78, 0.67],
            'Film C': [0.35, 0.78, 1.00, 0.94],
            'Film D': [0.81, 0.67, 0.94, 1.00]
        }, index=['Film A', 'Film B', 'Film C', 'Film D']).style.background_gradient(cmap='Blues'))
    
    # Guide d'utilisation dans une card
    st.markdown("""
    <div class='card'>
        <div class='card-header'>🚀 Comment utiliser cette application</div>
        <ol>
            <li><b>Page de Saisie</b> : Entrez des notations ou chargez un fichier CSV</li>
            <li><b>Analyse</b> : Le système calcule automatiquement les similarités</li>
            <li><b>Recommandations</b> : Obtenez des prédictions personnalisées</li>
        </ol>
        <div class='info-card' style='padding: 10px; margin-top: 15px;'>
            💡 Explorez les différentes pages via le menu latéral !
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page Streamlit
st.set_page_config(
    page_title="📊Système de Recommandation", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 
with st.sidebar : 
        st.markdown("""
        ## Auteurs
        Gandaho Merveilleux AZIHOU
        * LinkedIn : [Merveilleux AZIHOU](www.linkedin.com/in/gandaho-merveilleux-azihou-757849221)
        * Email : [merveilleuxazihou@gmail.com](merveilleuxazihou@gmail.com)
                    """)

# Style CSS
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
        .stButton>button {
            background-color: #4e73df;
            color: white;
            border-radius: 5px;
            padding: 8px 16px;
        }
        .stSlider>div>div>div>div {
            background-color: #4e73df;
        }
        .success-card {
            border-left: 4px solid #1cc88a;
        }
        .warning-card {
            border-left: 4px solid #f6c23e;
        }
        .error-card {
            border-left: 4px solid #e74a3b;
        }
        .info-card {
            border-left: 4px solid #36b9cc;
        }
    </style>
""", unsafe_allow_html=True)

# Titre principal avec style
st.markdown("""
    <div style='background-color: #4e73df; padding: 20px; border-radius: 10px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>Système de Recommandation de Films</h1>
    </div>
""", unsafe_allow_html=True)

# Menu horizontal
selected = option_menu(
    menu_title=None,
    options=["Manuelle", "Charger un fichier CSV"],
    icons=["pencil-square", "upload"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f8f9fc"},
        "icon": {"color": "#4e73df", "font-size": "18px"}, 
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#eaeaea"},
        "nav-link-selected": {"background-color": "#4e73df"},
    }
)

# Fonctions
def item_item_similarity(user_item_matrix):
    try:
        user_item_matrix = user_item_matrix.fillna(0)
        sparse_matrix = csr_matrix(user_item_matrix.values)
        item_similarity = cosine_similarity(sparse_matrix.T)
        item_similarity_df = pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)
        return item_similarity_df
    except Exception as e:
        st.error(f"Erreur lors du calcul de la similarité : {e}")
        return None

def get_top_n_recommendations(user_id, user_item_matrix, item_similarity_df, top_n):
    try:
        user_ratings = user_item_matrix.loc[user_id]
        recommendations = {}
        for item in user_item_matrix.columns:
            if pd.isna(user_ratings[item]):
                sim_scores = item_similarity_df[item]
                user_ratings_notna = user_ratings.dropna()
                recommendation_score = np.dot(sim_scores, user_ratings_notna) / sim_scores.sum()
                recommendations[item] = recommendation_score
        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return sorted_recommendations
    except Exception as e:
        st.error(f"Erreur lors du calcul des recommandations : {e}")
        return []

def predict_rating(user_id, item_id, user_item_matrix, item_similarity_df):
    try:
        user_ratings = user_item_matrix.loc[user_id]
        sim_scores = item_similarity_df[item_id]
        user_ratings_notna = user_ratings.dropna()
        sim_scores_filtered = sim_scores[user_ratings_notna.index]
        if sim_scores_filtered.sum() == 0:
            st.warning(f"Impossible de prédire la note pour l'item {item_id} : pas assez de données de similarité.")
            return None
        else:
            predicted_rating = np.dot(sim_scores_filtered, user_ratings_notna) / sim_scores_filtered.sum()
            return predicted_rating
    except Exception as e:
        st.error(f"Erreur lors de la prédiction de la note : {e}")
        return None

# Section pour les données manuelles
if selected == "Manuelle":
    with st.container():
        st.markdown("<div class='card'><div class='card-header'>📝 Entrez les notations manuellement</div>", unsafe_allow_html=True)
        
        # Configuration de base
        col1, col2 = st.columns(2)
        with col1:
            num_users = st.number_input("Nombre d'utilisateurs :", min_value=1, max_value=20, value=3, 
                                      help="Définissez le nombre d'utilisateurs qui ont noté les films")
        with col2:
            num_items = st.number_input("Nombre de films :", min_value=1, max_value=20, value=5,
                                      help="Définissez le nombre de films à noter")
        
        # Instructions claires
        with st.expander("ℹ️ Comment remplir le tableau", expanded=False):
            st.markdown("""
                <div class='info-card' style='padding: 15px; margin-bottom: 20px;'>
                    <ul>
                        <li>Chaque colonne représente un film différent</li>
                        <li>Chaque ligne correspond à un utilisateur différent</li>
                        <li>Entrez des notes entre 1 (pas aimé) et 5 (excellent)</li>
                        <li>Laissez vide si l'utilisateur n'a pas vu le film</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # Tableau de saisie        
        data = pd.DataFrame(index=range(1, num_users + 1), columns=range(1, num_items + 1))
        
        # En-tête du tableau avec les films
        cols = st.columns(num_items)
        for item in range(1, num_items + 1):
            with cols[item-1]:
                st.markdown(f"""
                    <div style='text-align: center; padding: 5px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 5px;'>
                        <strong>Film #{item}</strong>
                    </div>
                """, unsafe_allow_html=True)
        
        # Saisie des notes avec meilleur visibilité
        for user in range(1, num_users + 1):
            st.markdown(f"<div style='margin: 10px 0 5px 0; font-weight: 500;'>Utilisateur {user}</div>", unsafe_allow_html=True)
            
            user_cols = st.columns(num_items)
            for item in range(1, num_items + 1):
                with user_cols[item-1]:
                    data.at[user, item] = st.number_input(
                        label=f"Note pour Film {item}",
                        min_value=1,
                        max_value=5,
                        value=None,
                        step=1,
                        key=f"user{user}_item{item}",
                        placeholder="1-5",
                        label_visibility="collapsed"
                    )
        
        # Conversion des données pour le traitement
        data_long = data.stack().reset_index()
        data_long.columns = ['user_id', 'item_id', 'rating']

# Section pour le chargement de fichier CSV
elif selected == "Charger un fichier CSV":
    with st.container():
        st.markdown("<div class='card'><div class='card-header'>Charger un fichier CSV</div>", unsafe_allow_html=True)
        
        with st.expander("ℹ️ Format du fichier CSV requis", expanded=False):
            st.markdown("""
                <div class='info-card' style='padding: 15px;'>
                    Le fichier CSV doit contenir les colonnes suivantes :
                    <ul>
                        <li><code>user_id</code> : Identifiant de l'utilisateur</li>
                        <li><code>item_id</code> : Identifiant du film</li>
                        <li><code>rating</code> : Note attribuée (1-5)</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=["csv"], label_visibility="collapsed")
        
        if uploaded_file is not None:
            try:
                data_long = pd.read_csv(uploaded_file)
                if not {'user_id', 'item_id', 'rating'}.issubset(data_long.columns):
                    st.markdown("<div class='error-card' style='padding: 15px;'>Le fichier CSV est incomplet. Vérifiez les colonnes requises.</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='success-card' style='padding: 15px;'>Fichier CSV chargé avec succès !</div>", unsafe_allow_html=True)
                    
                    with st.expander("👀 Aperçu des données chargées", expanded=True):
                        st.dataframe(data_long.head(10))
                    
                    # Convertir les données en matrice utilisateur-item
                    user_item_matrix = data_long.pivot(index='user_id', columns='item_id', values='rating')
                    
                    st.markdown("<div class='card' style='margin-top: 20px;'><div class='card-header'>Matrice des notations</div>", unsafe_allow_html=True)
                    st.caption("Les cases vides représentent les notes manquantes")
                    st.dataframe(user_item_matrix.style.highlight_null(color='#ffecec'))
                    st.markdown("</div>", unsafe_allow_html=True)
                    
            except Exception as e:
                st.markdown(f"<div class='error-card' style='padding: 15px;'>Erreur lors de la lecture du fichier : {e}</div>", unsafe_allow_html=True)

# Section pour le top-n et la recherche
if 'data_long' in locals():
    user_item_matrix = data_long.pivot(index='user_id', columns='item_id', values='rating')
    if not user_item_matrix.empty:
        with st.container():
            
            st.markdown("<div class='card' style='margin-top: 20px;'><div class='card-header'>Paramètres de recommandation</div>", unsafe_allow_html=True)
            top_n = st.slider("Nombre de recommandations (top-n) :", min_value=1, max_value=10, value=3)
            st.markdown("</div>", unsafe_allow_html=True)
            
            item_similarity_df = item_item_similarity(user_item_matrix)
            if item_similarity_df is not None:
                with st.expander("📊 Matrice de similarité entre les films", expanded=True):
                    fig, ax = plt.subplots(figsize=(10, 8))
                    sns.heatmap(item_similarity_df, annot=True, cmap="coolwarm", ax=ax)
                    st.pyplot(fig)
                
                st.markdown("<div class='card' style='margin-top: 20px;'><div class='card-header'>Prédiction de note</div>", unsafe_allow_html=True)
                user_id = st.number_input("ID de l'utilisateur :", min_value=1, max_value=len(user_item_matrix))
                item_id = st.number_input("ID du film à évaluer :", min_value=1)
                
                if st.button("Prédire la note"):
                    if item_id in user_item_matrix.columns:
                        if not pd.isna(user_item_matrix.at[user_id, item_id]):
                            st.markdown(f"""
                                <div class='info-card' style='padding: 15px;'>
                                    L'utilisateur {user_id} a déjà noté le film {item_id} avec la note <strong>{user_item_matrix.at[user_id, item_id]}</strong>.
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            predicted_rating = predict_rating(user_id, item_id, user_item_matrix, item_similarity_df)
                            if predicted_rating is not None:
                                if predicted_rating >= 3:
                                    st.markdown(f"""
                                        <div class='success-card' style='padding: 15px;'>
                                            <div style='font-size: 1.2rem; margin-bottom: 10px;'>Note prédite : {predicted_rating:.2f}/5</div>
                                            <div style='font-size: 1.5rem; text-align: center;'>❤️ Recommandé !</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown(f"""
                                        <div class='warning-card' style='padding: 15px;'>
                                            <div style='font-size: 1.2rem; margin-bottom: 10px;'>Note prédite : {predicted_rating:.2f}/5</div>
                                            <div style='font-size: 1.5rem; text-align: center;'>💔 Non recommandé</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='error-card' style='padding: 15px;'>Film non trouvé dans la base de données !</div>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='warning-card' style='padding: 15px;'>Veuillez charger ou entrer des données valides.</div>", unsafe_allow_html=True)
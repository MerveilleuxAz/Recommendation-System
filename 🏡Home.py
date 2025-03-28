# Basic code to run streamlit app
import streamlit as st

def main():
    st.set_page_config(
    page_title="🏡Home",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",
    )
    st.title("Recommendation System")
    st.subheader("The recommendation systems presented here is based on the collaborative filtering algorithm. It uses the overview of the item to recommend the similar items.")
    st.write("This is the page to test students on the recommendation system and how to deploy a user-friendly interface for it. Click each of the pages to see the different propositions.")
    with st.sidebar : 
        st.markdown("""
        ## Auteurs
        Gandaho Merveilleux AZIHOU
        * LinkedIn : [Merveilleux AZIHOU](www.linkedin.com/in/gandaho-merveilleux-azihou-757849221)
        * Email : [merveilleuxazihou@gmail.com](merveilleuxazihou@gmail.com)
                    """)

if __name__ == '__main__':
    main()
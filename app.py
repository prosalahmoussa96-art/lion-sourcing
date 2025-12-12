import streamlit as st
import pandas as pd

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Sourcing Lion", page_icon="🦁", layout="wide")

st.title("🦁 Lion Industrie - Sourcing Fournisseurs")
st.markdown("### Trouvez vos lots en quelques clics")
st.divider()

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    # On lit le fichier CSV avec le séparateur point-virgule
    try:
        df = pd.read_csv("data.csv", sep=";")
        return df
    except Exception as e:
        return None

df = load_data()

if df is None:
    st.error("⚠️ Erreur : Le fichier 'data.csv' est introuvable ou mal formaté.")
    st.stop()

# --- BARRE LATÉRALE (FILTRES) ---
st.sidebar.header("🔍 Critères de recherche")

# 1. Filtre Pays
all_countries = sorted(df['Pays'].unique())
selected_country = st.sidebar.multiselect("Pays d'origine", all_countries, default=all_countries)

# 2. Filtre Type (Indoor/Outdoor)
all_types = sorted(df['Type'].unique())
selected_type = st.sidebar.multiselect("Type de culture", all_types, default=all_types)

# 3. Filtre Prix
min_price = int(df['Prix'].min())
max_price = int(df['Prix'].max())
price_range = st.sidebar.slider("Budget Max (€/kg)", min_price, max_price, max_price)

# --- FILTRAGE DES DONNÉES ---
# On garde les lignes qui correspondent aux choix
filtered_df = df[
    (df['Pays'].isin(selected_country)) &
    (df['Type'].isin(selected_type)) &
    (df['Prix'] <= price_range)
]

# --- AFFICHAGE DES RÉSULTATS ---
col1, col2 = st.columns([1, 3])
with col1:
    st.metric(label="Offres trouvées", value=len(filtered_df))

st.subheader("📋 Liste des lots disponibles")

if not filtered_df.empty:
    # Affichage propre du tableau
    st.dataframe(
        filtered_df,
        column_config={
            "Nom": "Fournisseur",
            "Variété": "Fleur / Produit",
            "Prix": st.column_config.NumberColumn("Prix (€)", format="%d €"),
            "Lien": st.column_config.LinkColumn("Lien Catalogue"),
            "Date": st.column_config.DateColumn("Date Récolte", format="DD/MM/YYYY"),
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("Aucun résultat ne correspond à ces filtres. Essayez d'élargir la recherche.")

# Petit footer Lion
st.markdown("---")
st.caption("Lion Industrie Sourcing Tool • Données internes")

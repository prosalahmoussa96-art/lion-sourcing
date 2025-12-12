import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Sourcing Lion V2", page_icon="🦁", layout="wide")

st.title("🦁 Lion Industrie - Sourcing Multi-Produits")
st.markdown("### Fleurs, Extraits, Comestibles & Vape")
st.divider()

# --- CHARGEMENT ---
@st.cache_data
def load_data():
    try:
        # On lit le CSV. Attention aux encodages parfois capricieux, ici on reste simple.
        df = pd.read_csv("data.csv", sep=";")
        return df
    except Exception as e:
        return None

df = load_data()

if df is None:
    st.error("⚠️ Erreur : Problème avec le fichier data.csv")
    st.stop()

# --- BARRE LATÉRALE (FILTRES INTELLIGENTS) ---
st.sidebar.header("🔍 Filtres")

# 1. Filtre CATEGORIE (Le plus important maintenant)
# Cela permet de choisir d'abord "Fleurs" ou "Comestibles"
all_cats = sorted(df['Categorie'].unique())
selected_cat = st.sidebar.multiselect("📂 Catégorie", all_cats, default=all_cats)

# 2. Filtre PAYS
# On ne montre que les pays disponibles pour les catégories choisies (optionnel mais plus propre)
available_countries = df[df['Categorie'].isin(selected_cat)]['Pays'].unique()
selected_country = st.sidebar.multiselect("🌍 Pays", available_countries, default=available_countries)

# 3. Filtre TYPE (Indoor, Distillat, Gummies...)
available_types = df[df['Categorie'].isin(selected_cat)]['Type'].unique()
selected_type = st.sidebar.multiselect("🏷️ Type / Méthode", available_types, default=available_types)

# 4. Filtre PRIX
# Attention : le prix peut être au kg ou à l'unité selon le produit
min_price = int(df['Prix'].min())
max_price = int(df['Prix'].max())
price_range = st.sidebar.slider("💰 Budget Max (Unité ou Kg)", min_price, max_price, max_price)

# --- FILTRAGE ---
filtered_df = df[
    (df['Categorie'].isin(selected_cat)) &
    (df['Pays'].isin(selected_country)) &
    (df['Type'].isin(selected_type)) &
    (df['Prix'] <= price_range)
]

# --- RÉSULTATS ---
col1, col2 = st.columns([1, 3])
with col1:
    st.metric(label="Offres trouvées", value=len(filtered_df))

st.subheader("📋 Résultats")

if not filtered_df.empty:
    st.dataframe(
        filtered_df,
        column_config={
            "Categorie": "Catégorie",
            "Nom": "Fournisseur",
            "Type": "Type/Méthode",
            "Prix": st.column_config.NumberColumn("Prix", format="%d €"),
            "Lien": st.column_config.LinkColumn("Lien Catalogue"),
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("Aucun produit trouvé avec ces critères.")

st.markdown("---")
st.caption("Lion Industrie • Base de données multi-produits")

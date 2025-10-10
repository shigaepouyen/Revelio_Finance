# prototype_app.py
import streamlit as st
import pandas as pd
# Rendre le module backend accessible lorsque l'app est lancée depuis ce sous-dossier
import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from backend.ofx_parser import parse_ofx

st.set_page_config(layout="wide")
st.title("📊 Revelio Finance - Prototype de Visionneuse OFX")

# --- Fonctions de Catégorisation ---
def apply_rules(description):
    """Applique des règles simples pour une catégorisation automatique."""
    description = description.lower()
    if "netflix" in description:
        return "Abonnements"
    if "amazon" in description or "amzn" in description:
        return "Shopping en ligne"
    if "sfr" in description or "orange" in description or "bouygues" in description:
        return "Factures (Télécom)"
    if "leclerc" in description or "carrefour" in description or "super u" in description:
        return "Courses"
    return "Non Catégorisé"

# --- Interface Utilisateur ---
uploaded_file = st.file_uploader("Choisissez un fichier OFX", type=["ofx", "qfx"])

if uploaded_file is not None:
    st.success("Fichier téléversé avec succès!")
    
    # Lire le contenu et utiliser le parser pour extraire les transactions
    file_bytes = uploaded_file.read()
    uploaded_file.seek(0)
    transactions = parse_ofx(file_bytes)
    
    if transactions:
        # Convertir en DataFrame Pandas pour un affichage facile
        df = pd.DataFrame(transactions)
        
        # Appliquer la catégorisation par règles
        df['categorie_auto'] = df['description'].apply(apply_rules)
        
        st.subheader(f"{len(df)} transactions trouvées")
        
        # Afficher le tableau des transactions
        st.dataframe(df)
        
        # Section pour la catégorisation manuelle (simplifiée pour le prototype)
        st.subheader("Catégorisation Manuelle")
        
        # Créer une copie pour l'édition
        df_editable = df.copy()
        
        # Liste des catégories possibles
        categories_list = [
            "Non Catégorisé",
            "Abonnements",
            "Shopping en ligne",
            "Factures (Télécom)",
            "Courses",
            "Transport",
            "Loisirs",
            "Restauration",
            "Santé",
            "Autres"
        ]
        
        # Créer une colonne pour la catégorie manuelle
        df_editable['categorie_manuelle'] = ""

        for i in df_editable.index:
            # Utiliser la catégorie auto comme défaut
            default_index = categories_list.index(df_editable.loc[i, 'categorie_auto']) if df_editable.loc[i, 'categorie_auto'] in categories_list else 0
            
            # Créer un selecteur pour chaque transaction
            selected_category = st.selectbox(
                f"Transaction: {df_editable.loc[i, 'date']} - {df_editable.loc[i, 'description']} ({df_editable.loc[i, 'amount']} €)",
                options=categories_list,
                index=default_index,
                key=f"cat_{i}" # Clé unique pour chaque widget
            )
            df_editable.loc[i, 'categorie_manuelle'] = selected_category
            
        st.subheader("Résultat de la Catégorisation Manuelle")
        st.dataframe(df_editable[['date', 'description', 'amount', 'categorie_manuelle']])
        
    else:
        st.error("Aucune transaction n'a pu être extraite du fichier. Le format est peut-être invalide.")

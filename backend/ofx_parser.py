# backend/ofx_parser.py

import io
from ofxtools.parser import OFXTree

def parse_ofx(file_content: bytes):
    """
    Analyse le contenu binaire d'un fichier OFX et retourne une liste de transactions.
    """
    try:
        tree = OFXTree()
        # Utiliser io.BytesIO pour lire le contenu binaire comme un fichier
        tree.parse(io.BytesIO(file_content))
        
        # Convertir les données OFX en objets Python plus simples
        response = tree.convert()
        
        # Accéder à la liste des transactions
        # La structure peut varier légèrement, mais c'est le chemin le plus courant
        statement = response.accounts[0].statement
        transactions = statement.transactions
        
        # Préparer la liste des résultats
        transaction_list = []
        for trn in transactions:
            transaction_list.append({
                "date": trn.dtposted.strftime('%Y-%m-%d'),
                "amount": float(trn.trnamt),
                "description": trn.memo
            })

        return transaction_list

    except Exception as e:
        # En cas d'erreur de parsing, retourner une liste vide ou gérer l'erreur
        print(f"Erreur lors du parsing du fichier OFX : {e}")
        return []
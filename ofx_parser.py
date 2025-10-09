# ofx_parser.py
from ofxtools.Parser import OFXTree
from decimal import Decimal
from datetime import datetime
import logging

# Configuration du logging pour ignorer les messages de débogage de la bibliothèque
logging.basicConfig(level=logging.INFO)

def parse_ofx(file_path):
    """
    Analyse un fichier OFX et retourne une liste de transactions.
    
    Args:
        file_path (str or file-like object): Le chemin vers le fichier OFX ou un objet fichier.
        
    Returns:
        list: Une liste de dictionnaires, chaque dictionnaire représentant une transaction.
    """
    transactions =
    parser = OFXTree()
    
    try:
        # Analyse le fichier (peut être un chemin ou un objet binaire)
        parser.parse(file_path)
        ofx = parser.convert()
        
        # Accède à la liste des transactions
        # La structure peut varier, on cherche dans les relevés de compte ou de carte de crédit
        transaction_lists =
        if hasattr(ofx, 'statements'):
            for stmt in ofx.statements:
                transaction_lists.append(stmt.banktranlist)
        if hasattr(ofx, 'creditcard_statements'):
             for stmt in ofx.creditcard_statements:
                transaction_lists.append(stmt.banktranlist)

        for tran_list in transaction_lists:
            for t in tran_list:
                transaction_data = {
                    "fitid": t.fitid,  # Identifiant unique de la transaction
                    "date": t.dtposted.strftime('%Y-%m-%d'),
                    "description": t.name or t.memo,
                    "amount": float(t.trnamt),
                    "type": t.trntype.lower()
                }
                transactions.append(transaction_data)
        
        # Trier les transactions par date, de la plus récente à la plus ancienne
        transactions.sort(key=lambda x: x['date'], reverse=True)
        
        return transactions

    except Exception as e:
        logging.error(f"Erreur lors de l'analyse du fichier OFX : {e}")
        return

if __name__ == '__main__':
    # Exemple d'utilisation : remplacez 'votre_fichier.ofx' par un vrai fichier
    # transactions_list = parse_ofx('votre_fichier.ofx')
    # if transactions_list:
    #     for trans in transactions_list:
    #         print(trans)
    pass
# backend/ofx_parser.py

import io
import logging
import re
from ofxtools.Parser import OFXTree
from datetime import datetime

logger = logging.getLogger(__name__)

def parse_ofx(file_content: bytes):
    """
    Analyse le contenu binaire d'un fichier OFX, le nettoie et retourne une liste de transactions.
    """
    try:
        # Tenter de décoder avec cp1252, sinon latin-1
        try:
            content_str = file_content.decode('cp1252')
        except UnicodeDecodeError:
            content_str = file_content.decode('latin-1')

        # 1. Nettoyer les données superflues après la balise </OFX>
        closing_tag = '</OFX>'
        closing_tag_index = content_str.rfind(closing_tag)
        if closing_tag_index != -1:
            content_str = content_str[:closing_tag_index + len(closing_tag)]
        
        # 2. Injecter la balise <LEDGERBAL> manquante au bon endroit si nécessaire
        if '<LEDGERBAL>' not in content_str:
            dtend_match = re.search(r'<DTEND>(\d+)', content_str)
            # Utiliser la date du relevé ou la date actuelle
            dtasof_str = dtend_match.group(1) if dtend_match else datetime.now().strftime('%Y%m%d%H%M%S')
            # La spec OFX requiert une heure, ajoutons-la si elle est absente
            if len(dtasof_str) == 8:
                dtasof_str += '120000'

            ledgerbal_tag = f'<LEDGERBAL><BALAMT>0.00<DTASOF>{dtasof_str}</DTASOF></LEDGERBAL>'

            banktranlist_closing_tag = '</BANKTRANLIST>'
            if banktranlist_closing_tag in content_str:
                content_str = content_str.replace(banktranlist_closing_tag, banktranlist_closing_tag + ledgerbal_tag)

        cleaned_content = content_str.encode('latin-1')

        tree = OFXTree()
        tree.parse(io.BytesIO(cleaned_content))
        response = tree.convert()

        # Utilisation de l'API de haut niveau "statements" pour une extraction robuste
        statements = getattr(response, 'statements', [])
        if not statements:
            logger.warning("Aucun relevé (statement) n'a été trouvé dans le fichier OFX.")
            return []
        
        # On prend le premier relevé trouvé dans le fichier
        statement = statements[0]

        transactions = getattr(statement, 'transactions', [])
        if not transactions:
            logger.warning("Le relevé a été trouvé, mais il ne contient aucune transaction.")
            return []

        transaction_list = []
        for trn in transactions:
            transaction_list.append({
                "date": trn.dtposted.strftime('%Y-%m-%d'),
                "amount": float(trn.trnamt),
                "description": trn.memo
            })

        return transaction_list

    except Exception as e:
        logger.error(f"Erreur détaillée lors du parsing du fichier OFX : {e}", exc_info=True)
        return []
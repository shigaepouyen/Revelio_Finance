# backend/ai_service.py

import httpx
import json
import logging
import re
from .schemas import CategorizationResponse

OLLAMA_API_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "llama3.2:3b"

logger = logging.getLogger(__name__)

async def categorize_transaction(description: str) -> CategorizationResponse:
    """
    Interacts with the Ollama API to categorize a transaction based on its description.
    Includes detailed logging and an increased timeout.
    """
    prompt = f"""
    SYSTEM: Tu es un expert comptable. Analyse le libellé de transaction suivant.
    Retourne **UNIQUEMENT** un objet JSON valide avec les clés "marchand_probable", "categorie_suggeree", et "ville".
    La catégorie DOIT être une de ces valeurs : [Alimentation, Logement, Transport, Loisirs, Santé, Abonnements, Autre].
    Ne fournis aucune explication ou texte en dehors de l'objet JSON.

    USER: {description}
    """

    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    # --- MODIFICATION CI-DESSOUS ---
    # Augmentation du timeout à 60 secondes pour laisser le temps au modèle de répondre.
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            logger.info(f"Sending request to Ollama for description: '{description}'")
            response = await client.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()

            response_text = response.text.strip()
            logger.info(f"===== RAW RESPONSE FROM OLLAMA =====\n{response_text}\n====================================")
            
            try:
                # Étape 1 : Extraire le contenu de la clé "response"
                llm_output_str = json.loads(response_text).get("response", "")
                if not llm_output_str:
                    logger.warning("The 'response' key from Ollama is empty.")
                    raise json.JSONDecodeError("Empty 'response' key from LLM", llm_output_str, 0)
                
                logger.info(f"--- Content of 'response' key ---\n{llm_output_str}\n---------------------------------")

                # Étape 2 : Utiliser une expression régulière pour trouver le JSON dans la chaîne
                match = re.search(r'\{.*\}', llm_output_str, re.DOTALL)
                
                if not match:
                    logger.warning("No JSON object found in the LLM response string.")
                    raise json.JSONDecodeError("No JSON object found in LLM response string", llm_output_str, 0)
                
                json_string_cleaned = match.group(0)
                logger.info(f"--- Cleaned JSON string found ---\n{json_string_cleaned}\n---------------------------------")
                
                # Étape 3 : Parser le JSON nettoyé
                data = json.loads(json_string_cleaned)
                logger.info("Successfully parsed the cleaned JSON.")
                return CategorizationResponse(**data)

            except (json.JSONDecodeError, TypeError) as e:
                logger.error(f"Failed to parse JSON response from LLM: {repr(e)}. Falling back to default.")
                return CategorizationResponse(marchand_probable="Unknown", categorie_suggeree="Autre", ville=None)

        except httpx.RequestError as e:
            # Modification du log pour avoir plus de détails sur l'erreur
            logger.error(f"Ollama request failed: {repr(e)}. Falling back to default.")
            return CategorizationResponse(marchand_probable="Unknown", categorie_suggeree="Autre", ville=None)

async def analyze_anomaly(transaction: dict, history: dict) -> dict:
    """
    Interacts with the Ollama API to detect anomalies in transactions.
    """
    # This will be a mock implementation for now.
    return {"est_anomalie": False, "justification": "Not implemented yet."}
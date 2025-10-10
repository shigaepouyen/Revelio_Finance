# backend/ai_service.py

import httpx
import json
import logging
from .schemas import CategorizationResponse

OLLAMA_API_URL = "http://host.docker.internal:11434/api/generate"
LLM_MODEL = "llama3:8b"

logger = logging.getLogger(__name__)

async def categorize_transaction(description: str) -> CategorizationResponse:
    """
    Interacts with the Ollama API to categorize a transaction based on its description.

    This function now uses a more reliable localhost address for Ollama (`host.docker.internal`)
    and includes robust error handling and JSON parsing.
    """
    prompt = f"""
    SYSTEM: Tu es un expert comptable spécialisé dans l'analyse de transactions bancaires. Analyse le libellé de transaction suivant et retourne **uniquement** un objet JSON valide. L'objet doit contenir les clés "marchand_probable" (string), "categorie_suggeree" (string), et "ville" (string, ou null si non détectée). La catégorie doit être choisie exclusivement dans cette liste : [Alimentation, Logement, Transport, Loisirs, Santé, Abonnements, Autre].

    USER: {description}
    """

    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()

            # The response from Ollama is a stream of JSON objects, we take the last one
            response_text = response.text.strip()
            # Attempt to parse the full response as JSON
            try:
                # The response from Ollama is a JSON object with a "response" key containing the actual JSON string
                json_response_str = json.loads(response_text).get("response", "{}")
                # Now parse the nested JSON string
                data = json.loads(json_response_str)
                return CategorizationResponse(**data)
            except (json.JSONDecodeError, TypeError) as e:
                logger.error(f"Failed to parse JSON response from LLM: {e}. Response text: '{response_text}'")
                # Fallback if JSON is malformed
                return CategorizationResponse(marchand_probable="Unknown", categorie_suggeree="Autre", ville=None)

        except httpx.RequestError as e:
            logger.error(f"Error requesting categorization from Ollama: {e}")
            # Fallback in case of network error
            return CategorizationResponse(marchand_probable="Unknown", categorie_suggeree="Autre", ville=None)

async def analyze_anomaly(transaction: dict, history: dict) -> dict:
    """
    Interacts with the Ollama API to detect anomalies in transactions.
    """
    # This will be a mock implementation for now.
    return {"est_anomalie": False, "justification": "Not implemented yet."}
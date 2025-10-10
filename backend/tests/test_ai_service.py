import pytest
import respx
from httpx import Response, RequestError
import json
from backend.ai_service import categorize_transaction
from backend.schemas import CategorizationResponse

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio

OLLAMA_API_URL = "http://host.docker.internal:11434/api/generate"

@respx.mock
async def test_categorize_transaction_success():
    """
    Tests successful categorization when the LLM returns a valid JSON response.
    """
    description = "PAIEMENT CB 22/07 STARBUCKS PARIS 11"
    mock_llm_response = {
        "marchand_probable": "Starbucks",
        "categorie_suggeree": "Restauration",
        "ville": "Paris 11"
    }
    # The Ollama API wraps the JSON response in a "response" key
    mock_api_response = {"response": json.dumps(mock_llm_response)}

    # Mock the API call
    respx.post(OLLAMA_API_URL).mock(return_value=Response(200, json=mock_api_response))

    # Call the function
    result = await categorize_transaction(description)

    # Assertions
    assert isinstance(result, CategorizationResponse)
    assert result.marchand_probable == "Starbucks"
    assert result.categorie_suggeree == "Restauration"
    assert result.ville == "Paris 11"

@respx.mock
async def test_categorize_transaction_invalid_json():
    """
    Tests the fallback mechanism when the LLM returns a malformed JSON string.
    """
    description = "Some garbled transaction"
    # The response from the API is not valid JSON
    mock_api_response = {"response": "this is not json"}

    respx.post(OLLAMA_API_URL).mock(return_value=Response(200, json=mock_api_response))

    result = await categorize_transaction(description)

    # Assertions for fallback behavior
    assert isinstance(result, CategorizationResponse)
    assert result.marchand_probable == "Unknown"
    assert result.categorie_suggeree == "Autre"
    assert result.ville is None

@respx.mock
async def test_categorize_transaction_network_error():
    """
    Tests the fallback mechanism when a network error occurs while calling the API.
    """
    description = "Transaction during network failure"

    # Mock a network error by raising httpx.RequestError
    respx.post(OLLAMA_API_URL).mock(side_effect=RequestError("Simulated network error", request=None))

    result = await categorize_transaction(description)

    # Assertions for fallback behavior
    assert isinstance(result, CategorizationResponse)
    assert result.marchand_probable == "Unknown"
    assert result.categorie_suggeree == "Autre"
    assert result.ville is None
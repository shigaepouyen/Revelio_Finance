# backend/routers/ai.py

from fastapi import APIRouter, HTTPException, Body
from ..schemas import TransactionDescription, CategorizationResponse
from ..ai_service import categorize_transaction, analyze_anomaly

router = APIRouter()

@router.post("/ai/categorize", response_model=CategorizationResponse)
async def categorize(transaction_desc: TransactionDescription):
    """
    Endpoint to categorize a single transaction description using the AI service.
    """
    if not transaction_desc.libelle:
        raise HTTPException(status_code=400, detail="Transaction description ('libelle') cannot be empty.")

    response = await categorize_transaction(transaction_desc.libelle)
    return response

@router.post("/ai/analyze-anomaly")
async def analyze_anomaly_endpoint(payload: dict = Body(...)):
    """
    Endpoint to analyze a transaction for anomalies.
    This is a mock implementation as per the plan.
    """
    # Extract data from payload - assuming a certain structure for now
    transaction_actuelle = payload.get("transaction_actuelle", {})
    historique_categorie = payload.get("historique_categorie", {})

    if not transaction_actuelle:
        raise HTTPException(status_code=400, detail="Payload must contain 'transaction_actuelle'.")

    # Call the mock service
    response = await analyze_anomaly(transaction_actuelle, historique_categorie)
    return response
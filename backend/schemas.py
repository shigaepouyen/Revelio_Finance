# backend/schemas.py

from pydantic import BaseModel
from typing import Optional

class TransactionDescription(BaseModel):
    """
    Pydantic model for the request payload of the categorization endpoint.
    """
    libelle: str

class CategorizationResponse(BaseModel):
    """
    Pydantic model for the response payload of the categorization endpoint.
    """
    marchand_probable: str
    categorie_suggeree: str
    ville: Optional[str] = None
# backend/main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .ofx_parser import parse_ofx
from .routers import ai
from .ai_service import categorize_transaction
import asyncio
import uvicorn

app = FastAPI(
    title="Revelio Finance API",
    description="API pour analyser les fichiers de transactions OFX.",
    version="1.0.0"
)

# Include AI routes
app.include_router(ai.router)

# Configuration CORS pour autoriser le frontend à communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Attention: En production, spécifiez les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get_index():
    """Serves the frontend index.html file."""
    return FileResponse('frontend/index.html')

@app.post("/upload-ofx/")
async def upload_ofx_file(file: UploadFile = File(...)):
    """
    Endpoint to upload an OFX file, parse it, enrich transactions with AI categorization,
    and return the result.
    """
    # Verify file type
    if not file.filename.lower().endswith(('.ofx', '.qfx')):
        raise HTTPException(status_code=400, detail="Invalid file type. Please provide a .ofx or .qfx file.")

    # Read file content
    file_content = await file.read()

    # Call the parsing function
    transactions = parse_ofx(file_content)

    if not transactions:
        raise HTTPException(status_code=400, detail="Could not parse file or no transactions found.")

    # Create a list of categorization tasks to run concurrently
    categorization_tasks = [categorize_transaction(trn["description"]) for trn in transactions]

    # Run all tasks in parallel
    enriched_data = await asyncio.gather(*categorization_tasks)

    # Combine original transaction data with enriched data
    enriched_transactions = []
    for i, trn in enumerate(transactions):
        enrichment = enriched_data[i]
        trn.update({
            "marchand_probable": enrichment.marchand_probable,
            "categorie_suggeree": enrichment.categorie_suggeree,
            "ville": enrichment.ville
        })
        enriched_transactions.append(trn)

    return {
        "filename": file.filename,
        "transaction_count": len(enriched_transactions),
        "transactions": enriched_transactions
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
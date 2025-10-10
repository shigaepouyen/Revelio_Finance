# backend/main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .ofx_parser import parse_ofx
import uvicorn

app = FastAPI(
    title="Revelio Finance API",
    description="API pour analyser les fichiers de transactions OFX.",
    version="1.0.0"
)

# Configuration CORS pour autoriser le frontend à communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Attention: En production, spécifiez les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de Revelio Finance"}

@app.post("/upload-ofx/")
async def upload_ofx_file(file: UploadFile = File(...)):
    """
    Endpoint pour téléverser un fichier OFX, l'analyser et retourner les transactions.
    """
    # Vérifier que c'est bien un fichier OFX
    if not file.filename.lower().endswith(('.ofx', '.qfx')):
        raise HTTPException(status_code=400, detail="Type de fichier invalide. Veuillez fournir un fichier .ofx ou .qfx.")

    # Lire le contenu du fichier
    file_content = await file.read()

    # Appeler la fonction de parsing
    transactions = parse_ofx(file_content)

    if not transactions:
        raise HTTPException(status_code=400, detail="Impossible de parser le fichier ou aucune transaction trouvée.")

    return {
        "filename": file.filename,
        "transaction_count": len(transactions),
        "transactions": transactions
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
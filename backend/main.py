# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

from ofx_parser import parse_ofx # On réutilise notre parser

app = FastAPI(
    title="Finance App API",
    description="API pour la gestion des transactions financières à partir de fichiers OFX.",
    version="1.0.0"
)

# --- Configuration CORS ---
# Permet à notre frontend (qui sera sur un autre domaine/port) de communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, restreindre à l'URL du frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modèles de données (pour la validation et la documentation) ---
# Pas de modèles spécifiques pour l'instant, on retourne directement le dict

# --- Endpoints de l'API ---
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de l'application de finances personnelles"}

@app.post("/upload-ofx/")
async def upload_ofx_file(file: UploadFile = File(...)):
    """
    Endpoint pour téléverser un fichier OFX et retourner les transactions en JSON.
    """
    if not file.filename.lower().endswith(('.ofx', '.qfx')):
        raise HTTPException(status_code=400, detail="Format de fichier invalide. Seuls les.ofx et.qfx sont acceptés.")
    
    try:
        # Le parser a besoin d'un objet fichier binaire
        contents = await file.read()
        
        # On passe le contenu binaire directement au parser
        import io
        transactions = parse_ofx(io.BytesIO(contents))
        
        if not transactions:
            raise HTTPException(status_code=404, detail="Aucune transaction trouvée dans le fichier.")
            
        return {"filename": file.filename, "transactions": transactions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Une erreur est survenue lors du traitement du fichier : {e}")

# --- Lancement du serveur ---
if __name__ == "__main__":
    # Pour lancer : uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
# backend/main.py

from fastapi import FastAPI, File, UploadFile, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from .ofx_parser import parse_ofx
from .ai_service import categorize_transaction
import asyncio
import uvicorn
import json

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI(
    title="Revelio Finance API",
    description="API pour analyser les fichiers de transactions OFX avec suivi en temps réel.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get_index():
    """Sert le fichier frontend index.html."""
    return FileResponse('frontend/index.html')

@app.post("/parse-ofx/")
async def parse_ofx_file(file: UploadFile = File(...)):
    """
    Endpoint qui parse le fichier OFX et retourne les transactions brutes.
    L'enrichissement se fera via WebSocket.
    """
    if not file.filename.lower().endswith(('.ofx', '.qfx')):
        raise HTTPException(status_code=400, detail="Type de fichier invalide.")

    file_content = await file.read()
    transactions = parse_ofx(file_content)

    if not transactions:
        raise HTTPException(status_code=400, detail="Impossible de parser le fichier ou aucune transaction trouvée.")

    return {
        "filename": file.filename,
        "transaction_count": len(transactions),
        "transactions": transactions
    }

@app.websocket("/ws/analyze")
async def websocket_analyze(websocket: WebSocket):
    """
    Endpoint WebSocket qui reçoit des transactions brutes, les enrichit par lots,
    et renvoie la progression en temps réel.
    """
    await websocket.accept()
    try:
        # 1. Attendre de recevoir la liste des transactions du client
        data = await websocket.receive_text()
        transactions_to_process = json.loads(data)
        
        total_transactions = len(transactions_to_process)
        BATCH_SIZE = 4 # Gardons une taille de lot raisonnable
        
        # 2. Traiter les transactions par lots et renvoyer la progression
        for i in range(0, total_transactions, BATCH_SIZE):
            batch_transactions = transactions_to_process[i:i + BATCH_SIZE]
            tasks = [categorize_transaction(trn["description"]) for trn in batch_transactions]
            
            # Exécuter le lot en parallèle
            batch_results = await asyncio.gather(*tasks)
            
            # Préparer les données enrichies pour ce lot
            enriched_batch = []
            for j, enrichment in enumerate(batch_results):
                trn = batch_transactions[j]
                trn.update({
                    "marchand_probable": enrichment.marchand_probable,
                    "categorie_suggeree": enrichment.categorie_suggeree,
                    "ville": enrichment.ville
                })
                enriched_batch.append(trn)

            # Calculer la progression
            progress = min(((i + BATCH_SIZE) / total_transactions) * 100, 100)

            # Envoyer le message de progression au client
            await websocket.send_json({
                "type": "progress",
                "processed_count": min(i + BATCH_SIZE, total_transactions),
                "total_count": total_transactions,
                "progress_percent": round(progress),
                "data": enriched_batch
            })
            
        # 3. Envoyer un message final
        await websocket.send_json({"type": "complete", "message": "Analyse terminée !"})

    except WebSocketDisconnect:
        logging.info("Client déconnecté.")
    except Exception as e:
        logging.error(f"Erreur WebSocket: {e}")
        await websocket.send_json({"type": "error", "message": str(e)})
    finally:
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
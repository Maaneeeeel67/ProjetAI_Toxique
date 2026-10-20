from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import time
import requests
import os
from .interface import predict_toxicity, predict_toxicity_detailed

app = FastAPI(title="Toxic Comment Moderation API", version="1.0")

THRESHOLD_BLOCK = 0.50  # Seuil de blocage à 50%

# --- CONFIGURATION INSTAGRAM / META ---
# Ce token sera utilisé pour valider la connexion avec Meta
META_VERIFY_TOKEN = "toxicguard_pfa_token_2026" 
# Ce token servira à donner l'ordre de suppression (Vous le générerez sur Meta plus tard)
META_ACCESS_TOKEN = "VOTRE_ACCESS_TOKEN_META_ICI"
# --------------------------------------

class ModerateRequest(BaseModel):
    text: str

class ModerateResponse(BaseModel):
    decision: str
    toxicity_score: float
    latency_ms: int
    categories: dict = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/moderate", response_model=ModerateResponse)
def moderate(req: ModerateRequest):
    start = time.time()
    text = req.text.strip()

    if not text:
        return {"decision": "REJECT", "toxicity_score": 0.0, "latency_ms": int((time.time()-start)*1000), "categories": {}}

    score, categories = predict_toxicity_detailed(text)
    decision = "BLOCK" if score >= THRESHOLD_BLOCK else "ALLOW"

    latency = int((time.time() - start) * 1000)
    return {"decision": decision, "toxicity_score": score, "latency_ms": latency, "categories": categories}

# ==========================================
# ROUTES POUR L'INTÉGRATION INSTAGRAM (META)
# ==========================================

@app.get("/webhook")
def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    """
    Étape 1 : Meta appelle cette route pour vérifier que l'API vous appartient.
    """
    if hub_mode == "subscribe" and hub_verify_token == META_VERIFY_TOKEN:
        print("✅ Webhook Instagram vérifié avec succès !")
        return PlainTextResponse(content=hub_challenge)
    raise HTTPException(status_code=403, detail="Token de vérification invalide")

@app.post("/webhook")
async def receive_instagram_comment(request: Request):
    """
    Étape 2 : Instagram envoie les nouveaux commentaires ici.
    """
    payload = await request.json()
    
    try:
        # On navigue dans le JSON complexe envoyé par Instagram
        for entry in payload.get('entry', []):
            for change in entry.get('changes', []):
                value = change.get('value', {})
                
                # Vérifie s'il s'agit d'un nouveau commentaire
                if 'text' in value and 'id' in value:
                    comment_text = value['text']
                    comment_id = value['id']
                    
                    print(f"\n💬 Nouveau commentaire reçu d'Instagram: '{comment_text}'")
                    
                    # 1. On passe le texte à votre IA
                    score = predict_toxicity(comment_text)
                    print(f"🧠 Score de toxicité évalué : {score:.2%}")
                    
                    # 2. Si c'est toxique, on demande à Instagram de le supprimer/masquer
                    if score >= THRESHOLD_BLOCK:
                        print("🚫 Commentaire toxique ! Envoi de l'ordre de suppression à Instagram...")
                        delete_url = f"https://graph.facebook.com/v19.0/{comment_id}?access_token={META_ACCESS_TOKEN}"
                        response = requests.delete(delete_url)
                        
                        if response.status_code == 200:
                            print("✅ Commentaire supprimé avec succès sur Instagram !")
                        else:
                            print("❌ Échec de la suppression (Vérifiez le META_ACCESS_TOKEN).")
                    else:
                        print("✅ Commentaire sain, on le laisse en ligne.")
                        
    except Exception as e:
        print(f"Erreur lors du traitement du webhook : {e}")

    # Il faut toujours répondre 200 OK rapidement à Meta, sinon ils désactivent le webhook
    return {"status": "success"}
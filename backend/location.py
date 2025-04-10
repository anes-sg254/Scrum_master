from fastapi import APIRouter, Request, Header, HTTPException
from config_db import connect_to_db
from utils import decode_token
from datetime import datetime

router = APIRouter()

# Réserver un matériel
@router.post("/reserver")
async def reserver(request: Request, authorization: str = Header(None)):
    token = authorization.split(" ")[1]
    user_id = decode_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Token invalide.")

    data = await request.json()
    materiel_id = data["materiel_id"]
    date_fin = data.get("date_fin")

    conn = connect_to_db()
    cursor = conn.cursor()

    # Vérifie que le matériel est disponible
    cursor.execute("SELECT disponible FROM materiels WHERE id = %s", (materiel_id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Matériel introuvable.")
    if not result[0]:
        raise HTTPException(status_code=400, detail="Matériel non disponible.")

    # Crée la location
    cursor.execute("""
        INSERT INTO locations (user_id, materiel_id, date_debut, date_fin, statut)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, materiel_id, datetime.utcnow(), date_fin, "en attente"))

    # Met à jour la dispo du matériel
    cursor.execute("UPDATE materiels SET disponible = FALSE WHERE id = %s", (materiel_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": f"Réservation du matériel {materiel_id} effectuée."}


# Historique des locations d’un utilisateur
@router.get("/locations/{user_id}")
def get_location_history(user_id: int):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT l.id, m.nom, l.date_debut, l.date_fin, l.statut
        FROM locations l
        JOIN materiels m ON l.materiel_id = m.id
        WHERE l.user_id = %s
        ORDER BY l.date_debut DESC
    """, (user_id,))
    locations = cursor.fetchall()
    cursor.close()
    conn.close()

    return {"locations": [
        {
            "id": loc[0],
            "materiel": loc[1],
            "date_debut": str(loc[2]),
            "date_fin": str(loc[3]) if loc[3] else None,
            "statut": loc[4]
        }
        for loc in locations
    ]}


# Voir les matériels disponibles
@router.get("/materiels/disponibles")
def get_disponibles():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, categorie, description FROM materiels WHERE disponible = TRUE")
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return {"materiels": [
        {
            "id": m[0],
            "nom": m[1],
            "categorie": m[2],
            "description": m[3]
        }
        for m in result
    ]}


# Voir les matériels loués
@router.get("/materiels/loues")
def get_loues():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, categorie FROM materiels WHERE disponible = FALSE")
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return {"materiels": [
        {
            "id": m[0],
            "nom": m[1],
            "categorie": m[2]
        }
        for m in result
    ]}

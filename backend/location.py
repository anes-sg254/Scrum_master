from fastapi import APIRouter, Request, Header, HTTPException,Depends
from config_db import connect_to_db
from utils import decode_token,get_current_user
from datetime import datetime


router = APIRouter()


# Réserver un matériel (seuls les étudiants peuvent)
@router.post("/reserver")
async def reserver(request: Request, authorization: str = Header(None)):
    token = authorization.split(" ")[1]
    user_id = decode_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Token invalide")

    conn = connect_to_db()
    cursor = conn.cursor()

    # Vérifie que l'utilisateur est étudiant
    cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
    role = cursor.fetchone()
    if not role or role[0] != "etudiant":
        raise HTTPException(status_code=403, detail="Seuls les étudiants peuvent réserver.")

    data = await request.json()
    materiel_id = data["materiel_id"]
    date_fin = data.get("date_fin")

    # Vérifie la disponibilité du matériel
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

    # Met à jour la disponibilité du matériel
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
        } for loc in locations
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
        } for m in result
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
        } for m in result
    ]}


@router.get("/locationsad")
def get_all_pending_locations(user_id: int = Depends(get_current_user)):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Vérifie si l'utilisateur est admin
    cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
    role = cursor.fetchone()

    if not role or role[0] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé à l'admin")

    cursor.execute("""
        SELECT l.id, u.name, m.nom, l.date_debut, l.date_fin, l.statut
        FROM locations l
        JOIN users u ON l.user_id = u.id
        JOIN materiels m ON l.materiel_id = m.id
        WHERE l.statut = 'en attente'
        ORDER BY l.date_debut DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return {
        "locations": [
            {
                "id": r[0],
                "utilisateur": r[1],
                "materiel": r[2],
                "date_debut": str(r[3]),
                "date_fin": str(r[4]) if r[4] else None,
                "statut": r[5]
            } for r in rows
        ]
    }


#Valider ou refuser une réservation (admin uniquement)
@router.patch("/locationsad/{location_id}")
def update_location_status(location_id: int, status: str, authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    user_id = decode_token(token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Token invalide")

    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
    role = cursor.fetchone()
    if not role or role[0] != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé à l'admin.")

    # Met à jour le statut
    cursor.execute("""
        UPDATE locations
        SET statut = %s
        WHERE id = %s
    """, (status, location_id))

    # Si refusée, on remet le matériel dispo
    if status == "refusée":
        cursor.execute("""
            UPDATE materiels
            SET disponible = TRUE
            WHERE id = (SELECT materiel_id FROM locations WHERE id = %s)
        """, (location_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": f"Location {location_id} mise à jour avec statut : {status}"}

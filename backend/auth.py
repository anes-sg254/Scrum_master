from fastapi import APIRouter, Request, HTTPException
from config_db import connect_to_db
from utils import hash_password, verify_password, create_token

router = APIRouter()

#Inscription utilisateur
@router.post("/register")
async def register(request: Request): 
    data = await request.json()        
    name = data["name"]
    email = data["email"]
    password = data["password"]
    phone_number = data["phone_number"]

    hashed_pw = hash_password(password)

    conn = connect_to_db()
    cursor = conn.cursor()

    # Vérifie si l’email existe déjà
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email déjà utilisé.")

    # Vérifie si le numéro est déjà utilisé
    cursor.execute("SELECT * FROM users WHERE phone_number = %s", (phone_number,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Téléphone déjà utilisé.")

    # Insère l'utilisateur
    cursor.execute(
        "INSERT INTO users (name, email, phone_number, password) VALUES (%s, %s, %s, %s)", 
        (name, email, phone_number, hashed_pw)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Inscription réussie."}

# Connexion utilisateur
@router.post("/login")
async def login(request: Request):   
    data = await request.json()
    email = data["email"]
    password = data["password"]

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user or not verify_password(password, user[1]):
        raise HTTPException(status_code=401, detail="Identifiants invalides.")
    
    token = create_token(user[0])
    cursor.close()
    conn.close()

    return {"access_token": token, "user_id": user[0]}

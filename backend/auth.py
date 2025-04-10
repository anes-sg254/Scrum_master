from fastapi import APIRouter, Request, HTTPException,Header
from config_db import connect_to_db
from utils import hash_password, verify_password, create_token,decode_token

router = APIRouter()

# Inscription utilisateur avec rôle
@router.post("/register")
async def register(request: Request): 
    data = await request.json()        
    name = data["name"]
    email = data["email"]
    password = data["password"]
    role = data.get("role", "etudiant")  

    hashed_pw = hash_password(password)

    conn = connect_to_db()
    cursor = conn.cursor()

    # Vérifie si l’email existe déjà
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email déjà utilisé.")

    # Insère l'utilisateur avec le rôle
    cursor.execute(
        "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)", 
        (name, email, hashed_pw, role)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": f"Inscription réussie en tant que {role}."}

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


@router.get("/me")
def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token invalide")

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return {"id": user[0], "name": user[1], "role": user[2]}


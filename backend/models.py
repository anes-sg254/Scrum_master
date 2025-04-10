from config_db import connect_to_db

# Crée la table des utilisateurs
def create_users_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) DEFAULT 'etudiant'
                );
            """)
            conn.commit()
            print("Table 'users' créée/vérifiée.")
    except Exception as e:
        print(f"Erreur table users : {e}")


# Crée la table des matériels
def create_materiels_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS materiels (
                    id SERIAL PRIMARY KEY,
                    nom VARCHAR(100) NOT NULL,
                    categorie VARCHAR(50),
                    description TEXT,
                    disponible BOOLEAN DEFAULT TRUE
                );
            """)
            conn.commit()
            print("Table 'materiels' créée/vérifiée.")
    except Exception as e:
        print(f"Erreur table materiels : {e}")


# Crée la table des locations
def create_locations_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS locations (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    materiel_id INTEGER REFERENCES materiels(id),
                    date_debut TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    date_fin TIMESTAMP,
                    statut VARCHAR(20) DEFAULT 'en attente'
                );
            """)
            conn.commit()
            print("Table 'locations' créée/vérifiée.")
    except Exception as e:
        print(f"Erreur table locations : {e}")


# Fonction principale
def main():
    conn = connect_to_db()
    create_users_table(conn)
    create_materiels_table(conn)
    create_locations_table(conn)
    conn.close()
    print("Connexion fermée.")

if __name__ == "__main__":
    main()

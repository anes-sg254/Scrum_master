import psycopg2


host = "localhost"
dbname = "location" 
user = "postgres"
password = "msprepsi"
port = "5432"


def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
        )
        print("Connexion réussie à la base de données.")
        return conn
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        exit()

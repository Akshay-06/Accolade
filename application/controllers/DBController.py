# Controller to handle database interactions
import psycopg2

# Connecting to the DB
def connectToDB():
    conn = psycopg2.connect(
    host="localhost",
    database="Accolade",
    user="postgres",
    password="admin",
    port=5432
    )
    return conn

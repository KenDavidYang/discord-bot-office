import mysql.connector
from config import MYSQL_PASSWORD

cnx = mysql.connector.connect(
    user = "default_user",
    password = MYSQL_PASSWORD,
    host = "localhost",
    database = "discord"
)

def is_registered(user) -> bool:
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM users WHERE discord_id = %(discord_id)s", {"discord_id": user.id})
    result = cursor.fetchone()
    cursor.close()
    if result is None:
        return False
    else:
        return True

def close_db():
    if cnx.is_connected():
        cnx.close()
        print("Database connection closed.")
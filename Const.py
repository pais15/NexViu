from dataManager import *

app = Client(
    "NexViu",
    bot_token=os.getenv("BOT_TOKEN"),
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),

)
"""    workdir="/app", 
    in_memory=False"""
db_connect = {
    "user": os.getenv("USERDB"),
    "password": os.getenv("PDB"),
    "host": os.getenv("HOSTDB"),
    "port": os.getenv("PORTDB"),
    "database": os.getenv("NAMEDB"),
}

db = Database(**db_connect)
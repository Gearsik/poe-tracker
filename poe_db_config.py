import os
from dotenv import load_dotenv

#loads the .env file with user credentials
load_dotenv

poe_league = os.getenv("POE_LEAGUE", "Fate+of+the+Vaal")
poe_api = "https://poe.ninja/poe2/api/economy/exchange/current/overview?league=Fate+of+the+Vaal&type=Currency"

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "name": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD") 
}
import os
from dotenv import load_dotenv

#loads environment variables from the .env file
load_dotenv()

#poe api configuration
POE_API_URL = "https://poe.ninja/poe1/api/economy/exchange/current/overview?league=Allflame&type=Currency"

POE_LEAGUE = os.getenv("POE_LEAGUE", "Curse of the Allflame")

POE_API_PARAMS = {
    "league": POE_LEAGUE,
    "type": "Currency"
}

#PostgreSQL configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST" , "db"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD") 
}
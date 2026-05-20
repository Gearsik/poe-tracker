import requests
import psycopg
from datetime import datetime 
#requests is just a module allowing the script to work with HTTP/HTTPS
#used to assign date and time values to the data recieved for database purposes, 
#psycog needed for connecting python and postgresSQL

# creating a fuction to fetch and store data using a variable with the API for fetching the data from the poe.ninja website.
def fetch_store_api():
    poe_api = "https://poe.ninja/poe2/api/economy/exchange/current/overview?league=Fate+of+the+Vaal&type=Currency"

    try:
        api_response = requests.get(poe_api, timeout=10)
        api_response.raise_for_status() 

        poe_data = api_response.json()



print("Status Code" , api_response.status_code)

#simple if statement that checks the status of the api and prints the first 500 characters from the data it recieves if successful.
#if api_response.status_code == 200:
#       print("Success! Data received.")
#      print("First 500 characters:" , api_response.text[:500])
#else:
#        print("Failed. Error:" , api_response.text)

#create a variable that saves recivied stings of data in a json list 
if api_response.status_code == 200:
    poe_data = api_response.json()

    print("Keys in main object:" , list(poe_data.keys()))

    currency_name_lookup = {item["id"]: item["name"] for item in poe_data.get("items" , [])}

    for currency in poe_data.get("lines" , [])[:5]:
        currency_id = currency.get("id")
        name = currency_name_lookup.get(currency_id)
        value = currency.get("primaryValue")
        print(f"Currency: {name:<25} | Primary Value: {value}")

        snapshot_time = datetime.now()
        print("Snapshotted at: " , snapshot_time)


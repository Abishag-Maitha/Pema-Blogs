import os 
from dotenv import load_dotenv
import requests, json
load_dotenv()

BASE_URL= os.getenv('BASE_URL')

def get_quotes():
    response = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    if response.status_code == 200:
        quote = response.json()
        return quote
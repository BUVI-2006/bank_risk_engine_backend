import os 
import firebase_admin
from firebase_admin import credentials,firestore
from datetime import datetime ,timedelta
import http.client , urllib.parse
import json 
import time 


def init_firebase():

    firebase_key=json.loads(os.environ['FIREBASE_KEY'])
    cred=credentials.Certificate(firebase_key)



    firebase_admin.initialize_app(cred)

    db=firestore.client()

    return db 


def news_store(stock,db):
    LIMIT=3

    conn=http.client.HTTPSConnection('api.marketaux.com')
    params = urllib.parse.urlencode({
    'api_token': os.getenv("MARKET_API_KEY"),
    'symbols': stock,
    'limit': 3                      # limit 3 is constant (free tier)
    })
    conn.request('GET', '/v1/news/all?{}'.format(params))

    res=conn.getresponse()
    data=res.read()
    json_data=json.loads(data.decode('utf-8'))     #  loaded json data

    
   
    for i in range(LIMIT):           # different UUID = different article , same UUID= may or may not be the same 
        uuid=json_data["data"][i]['uuid']
        title=json_data["data"][i]['title']
        description=json_data["data"][i]['description']
        publish_date=json_data["data"][i]['published_at']

        docs=(db.collection("news").document(stock).collection("articles").document(uuid))

        docs.set({"uuid":uuid,"title":title,"description":description,"publish_date":publish_date})

    

    print(f"Stored {len(json_data.get('data', []))} articles for {stock}")




def run_job(db):
    stocks=['ABCB', 'ACNB', 'ALRS', 'AMAL', 'AMTB']
    end_time=datetime.utcnow() + timedelta(minutes=15)

    while datetime.utcnow() < end_time:
        for stock in stocks:
            try:
                news_store(stock,db)

            except Exception as e:
                print(f"Error:{e}")

        time.sleep(60)



if __name__=="__main__":
    db=init_firebase()
    run_job(db)

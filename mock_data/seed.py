import random
from datetime import datetime

from app.helpers import mongo_client

db = mongo_client()
names = db.list_collection_names()

# Create Mongo Collections
if 'clients' not in names:
    db.create_collection('clients')

if 'engagements' not in names:
    db.create_collection('engagements')

if 'interactions' not in names:
    db.create_collection('interactions')

# Seed Users
db.clients.delete_many({})
client1 = db.clients.insert_one({'name': 'Unicorns, LLC', 'nickname': 'uni'}).inserted_id
client2 = db.clients.insert_one({'name': 'Giraffes, Ltd.', 'nickname': 'raf'}).inserted_id

# Seed Engagements
db.engagements.delete_many({})
client1_engagement1 = db.engagements.insert_one({'clientId': client1, 'name': 'Phone'}).inserted_id
client1_engagement2 = db.engagements.insert_one({'clientId': client1, 'name': 'Chat Support'}).inserted_id

client2_engagement1 = db.engagements.insert_one({'clientId': client2, 'name': 'Phone Support'}).inserted_id
client2_engagement2 = db.engagements.insert_one({'clientId': client2, 'name': 'Twitter'}).inserted_id
client2_engagement3 = db.engagements.insert_one({'clientId': client2, 'name': 'Facebook'}).inserted_id

# Seed Interaction data
db.interactions.delete_many({})

first_names = ['John', 'Sally', 'Matt', 'Anthony', 'Stuart', 'Samantha', 'Jose', 'Abby', 'Shawna']
last_names = ['Smith', 'Jameson', 'Alexander', 'Ford', 'Montgomery', 'Newman', 'Trevino', 'Erickson']
sentiment_types = ['Negative', 'Neutral', 'Positive']

for engagement_id in [client1_engagement1, client1_engagement2, client2_engagement1, client2_engagement2, client2_engagement3]:
    for _ in range(50):
        random_sentiment = random.choice(sentiment_types)
        random_day = random.randint(1, 29)
        random_month = random.randint(1, 7)
        random_hour = random.randint(0, 23)
        random_date = datetime(2020, random_month, random_day, random_hour)

        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        random_name = first_name + ' ' + last_name

        interaction = {
            'engagementId': engagement_id,
            'interactionDate': random_date,
            'agentName': random_name,
            'sentiment': random_sentiment,
            'custom': {
                'csvName': f'{random_date.strftime("%Y_%d_%m")}_report.csv',
                'agentFirstName': first_name, 'agentLastName': last_name
            }
        }
        db.interactions.insert_one(interaction)

# topbox-backend-takehome-test

You can run this code locally or via Docker (see sections below).  
Please read the entire README before beginning.

If you wish to visualize the database, consider installing MongoDB Compass or Robo 3T

NOTE: You will need to use docker-compose to spin up the Mongo Database

## Mongo Schema Design
```
client
└── engagement
    └── interaction
```

### Client

This is self-explanatory. We have many clients who use the Topbox platform. This is where all global client properties reside.

- name
- nickName (shortened version of name)

### Engagement

The engagement collection is a logical separation of upstream client data. This allows us to separate client
  data by source: Twitter, Facebook, Phone Support, or Chat Support (it really just depends on what data the client wants to ingest into Topbox)

- clientId (foreign key: the client the engagement is associated with)
- name (name of the engagement: SMS, Chat, Facebook, Phone, etc.)

### Interaction

The `interaction` collection is where all custom client data is written to. This could be a chat log from an online chat session,
  a support phone call for a returned pair of shoes, or a tweet from Twitter.

- engagementId (foreign key: the engagement which the interaction data is associated with)
- agentName (the agent who made the phone call, the support agent who was in the chat session, etc.)
- interactionDate (the timestamp for the customer interaction - i.e. when a phone call began, when a tweet was sent)
- custom (this sub-document is where all original source data is dumped - agent name, csv name, etc.)

## Run via Docker

### Build
```.env
docker-compose build
```

### Run
```.env
docker-compose up
```

### Seed Data
```
docker-compose exec web python3 /web/mock_data/seed.py
```

### Other commands
```.env
docker-compose down  # tear down stack
```

## Running Locally

This repo should work with Python 3.6, 3.7, and 3.8

### Install requirements from setup.py
```
pip3 install -e .
```

### Run Locally
```
export MONGO_URI=mongodb://admin:adminpass@localhost:27017/production?authSource=admin
FLASK_APP=app/app.py flask run --port 5001
```

### Seed Data
```
export MONGO_URI=mongodb://admin:adminpass@localhost:27017/production?authSource=admin
python3 mock_data/seed.py
```


## Querying the API

### Via Bash

```
curl localhost:5000/clients
```

### Via Postman

https://www.postman.com/

## Example Responses

Querying `/interactions/<interaction_id>`

Will return the following
```json
{
  "_id": {
    "$oid": "5f18d12f42262eec0d43567d"
  },
  "engagementId": {
    "$oid": "5f18d12f42262eec0d435583"
  },
  "interactionDate": {
    "$date": 1589630400000
  },
  "agentName": "John Ford",
  "sentiment": "Negative",
  "custom": {
    "csvName": "2020_16_05_report.csv",
    "agentFirstName": "John",
    "agentLastName": "Ford"
  }
}
```
NOTE: This is BSON-encoded JSON (as you can see by the `"$date"` and `"$oid"` fields... BSON encoding works fine for this API)

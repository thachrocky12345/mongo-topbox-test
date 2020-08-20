from bson import json_util, ObjectId
import dateutil.parser
from flask import Flask
from flask import request

from app.helpers import mongo_client

API_VERSION = '1.0'

app = Flask(__name__)
db = mongo_client()


@app.route('/')
def root():
    response = {'apiVersion': API_VERSION, 'appName': 'Topbox Backend Take Home Test'}
    return json_util.dumps(response)


@app.route('/clients')
def clients():
    return json_util.dumps(db.clients.find({}))


@app.route('/clients/<client_id>')
def clients_by_id(client_id):
    client_object_id = ObjectId(client_id)
    return json_util.dumps(db.clients.find_one({'_id': client_object_id}))


@app.route('/engagements')
def engagements():
    return json_util.dumps(db.engagements.find({}))


@app.route('/engagements/<engagement_id>')
def engagements_by_id(engagement_id):
    engagement_object_id = ObjectId(engagement_id)
    return json_util.dumps(db.engagements.find_one({'_id': engagement_object_id}))


@app.route('/interactions')
def interactions():
    # TODO: Modify this endpoint according to problem statement!
    engagement_id = request.args.get("engagementId")
    if not engagement_id:
        raise ValueError("engagementId input is required")
    engagement_object_id = ObjectId(engagement_id)

    interaction_start_date = request.args.get("startDate")
    interaction_end_date = request.args.get("endDate")
    conditions = {
        "$and": [{"engagementId": engagement_object_id}]
    }

    if interaction_start_date:
        start_date = dateutil.parser.parse(interaction_start_date)
        conditions["$and"].append({'interactionDate': {'$gte': start_date}})
    if interaction_end_date:
        end_date = dateutil.parser.parse(interaction_end_date)
        conditions["$and"].append({'interactionDate': {'$lte': end_date}})

    ret_data = db.interactions.find(conditions)
    return json_util.dumps(ret_data)

@app.route('/interactions/<interaction_id>')
def interactions_by_id(interaction_id):
    interaction_object_id = ObjectId(interaction_id)
    return json_util.dumps(db.interactions.find_one({'_id': interaction_object_id}))

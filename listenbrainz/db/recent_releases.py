import requests
from flask import current_app


def insert_recent_releases(db_name, docs):
    couchdb_url = f"http://{current_app.config['COUCHDB_HOST']}:{current_app.config['COUCHDB_PORT']}/{db_name}/_bulk_docs"
    for doc in docs:
        doc["_id"] = str(doc["user_id"])
    response = requests.post(couchdb_url, json=docs)
    response.raise_for_status()


def get_recent_release_database_name():
    databases_url = f"http://{current_app.config['COUCHDB_HOST']}:{current_app.config['COUCHDB_PORT']}/_all_dbs"
    response = requests.get(databases_url)
    response.raise_for_status()
    databases = response.json()

    recent_release_dbs = [db for db in databases if db.startswith("recent_release")]
    return sorted(recent_release_dbs)[-1]


def get_recent_releases(user_id):
    database = get_recent_release_database_name()
    document_url = f"http://{current_app.config['COUCHDB_HOST']}:{current_app.config['COUCHDB_PORT']}/{database}/{user_id}"

    response = requests.get(document_url)
    response.raise_for_status()
    data = response.json()

    return {
        "user_id": user_id,
        "releases": data["releases"]
    }

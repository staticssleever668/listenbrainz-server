import requests
from flask import current_app


def get_couchdb_base_url():
    return f"http://{current_app.config['COUCHDB_USER']}" \
           f":{current_app.config['COUCHDB_ADMIN_KEY']}" \
           f"@{current_app.config['COUCHDB_HOST']}" \
           f":{current_app.config['COUCHDB_PORT']}"


def check_create_recent_release_database(db_name):
    databases_url = f"{get_couchdb_base_url()}/{db_name}"
    response = requests.head(databases_url)
    if response.status_code == 200:
        return

    response = requests.put(databases_url)
    response.raise_for_status()


def get_recent_release_database_name():
    databases_url = f"{get_couchdb_base_url()}/_all_dbs"
    response = requests.get(databases_url)
    response.raise_for_status()
    databases = response.json()

    recent_release_dbs = [db for db in databases if db.startswith("recent_release")]
    return sorted(recent_release_dbs)[-1]


def insert_recent_releases(db_name, docs):
    check_create_recent_release_database(db_name)
    couchdb_url = f"{get_couchdb_base_url()}/{db_name}/_bulk_docs"
    for doc in docs:
        doc["_id"] = str(doc["user_id"])
    response = requests.post(couchdb_url, json=docs)
    response.raise_for_status()


def get_recent_releases(user_id):
    database = get_recent_release_database_name()
    document_url = f"{get_couchdb_base_url()}/{database}/{user_id}"

    response = requests.get(document_url)
    response.raise_for_status()
    data = response.json()

    return {
        "user_id": user_id,
        "releases": data["releases"]
    }

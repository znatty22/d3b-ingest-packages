#!/usr/bin/env python

import os
import json
import argparse
from pprint import pprint

import requests

from config import (
    METABASE_SETUP_TEMPLATE,
    INGEST_DB_HOST,
    INGEST_DB_PORT,
    INGEST_VIEWER_USER,
    INGEST_VIEWER_PASSWORD,
    METABASE_APP_ADMIN,
    METABASE_APP_ADMIN_PASSWORD,
    METABASE_APP_ADMIN_EMAIL,
    METABASE_APP_URL,
)
from scripts import db


def setup_metabase(ingest_db, package_path):
    """
    Setup the first user in the metabase app. This will be the admin
    user
    Connect the ingest database to metabase
    """
    print("📊 Begin setting up metabase app ...")

    # Send request to get setup token
    print("🔐 Get setup token ...")
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.get(
            f"{METABASE_APP_URL}/api/session/properties",
            headers=headers
        )
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Problem fetching metabase setup token")
        print(resp.text)
        raise e

    token = resp.json()["setup-token"]

    # Send setup payload to bootstrap metabase
    print("💌 Send setup request ...")
    with open(METABASE_SETUP_TEMPLATE) as json_file:
        setup_payload = json.load(json_file)

    setup_payload["token"] = token
    setup_payload["user"].update(
        {
            "password": METABASE_APP_ADMIN_PASSWORD,
            "first_name": "Metabase Admin",
            "last_name": None,
            "email": METABASE_APP_ADMIN_EMAIL
        }
    )
    setup_payload["database"]["name"] = package_path
    setup_payload["database"]["details"] = {
        "host": INGEST_DB_HOST,
        "port": int(INGEST_DB_PORT),
        "dbname": ingest_db,
        "user": INGEST_VIEWER_USER,
        "password": INGEST_VIEWER_PASSWORD,
    }
    try:
        resp = requests.post(
            f"{METABASE_APP_URL}/api/setup",
            headers=headers,
            json=setup_payload
        )
        resp.raise_for_status()
        # session_token = resp.json()["id"]
    except requests.exceptions.HTTPError as e:
        print("Problem sending setup request to metabase")
        print(resp.text)
        raise e

    print("✅ Metabase app setup complete")


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Setup metabase app'
    )
    parser.add_argument(
        "ingest_db",
        help="The name of the database with ingested data that metabase "
        "will connect to",
    )
    parser.add_argument(
        "package_path",
        help="The path to the ingest package you want counts for. Path "
        "should be relative to d3b_ingest_packages/packages directory",
    )
    args = parser.parse_args()

    setup_metabase(args.ingest_db, args.package_path)


if __name__ == "__main__":
    cli()

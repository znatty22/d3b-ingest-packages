#!/usr/bin/env python

import os
import psycopg2
from psycopg2 import sql
import argparse

from config import (
    METABASE_DB_USER,
    METABASE_DB_PASSWORD,
)
from scripts import db


def init_db(metabase_db, username, password, hostname="localhost", port=5432):
    """
    Drop the db if exists and then create a new db
    Create the metabase app user
    """
    # Connect to postgres db
    conn = psycopg2.connect(
        dbname="postgres",
        user=username, password=password, host=hostname, port=port
    )

    # Drop the db if it exists and then create db
    db.drop_db(conn, metabase_db)

    # Create metabase app user with appropriate permissions
    print(f"Creating user {METABASE_DB_USER}, {METABASE_DB_PASSWORD}")
    db.create_user(conn, METABASE_DB_USER, METABASE_DB_PASSWORD)

    print(f"Creating database {metabase_db} ...")
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(
            sql.SQL(
                "CREATE DATABASE {0} WITH OWNER = {1};"
            ).format(
                sql.Identifier(metabase_db),
                sql.Identifier(METABASE_DB_USER),
            )
        )


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Initialize the metabase db'
    )
    parser.add_argument(
        "metabase_db",
        help="The name of the database where metabase app data will be"
        " data will go",
    )
    parser.add_argument(
        "-u", "--username",
        help="Super username to use when connecting to the database server",
        required=True,
    )
    parser.add_argument(
        "-w", "--password",
        help="Super user password to use when connecting to the database server",
        required=True,
    )
    parser.add_argument(
        "-n", "--hostname",
        help="Hostname of the database server to connect to",
        required=False,
        default="localhost",
    )
    parser.add_argument(
        "-p", "--port",
        help="Port of the database server to connect to",
        required=False,
        default=5432,
    )
    args = parser.parse_args()

    init_db(
        args.metabase_db,
        args.username,
        args.password,
        hostname=args.hostname,
        port=args.port
    )


if __name__ == "__main__":
    cli()

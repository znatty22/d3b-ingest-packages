#!/usr/bin/env python

import db
import argparse
import os
import psycopg2
from psycopg2 import sql

PG_ADMIN = os.environ["POSTGRES_ADMIN"]
PG_ADMIN_PASSWORD = os.environ["POSTGRES_ADMIN_PASSWORD"]


def init_metabase_db(
    db_name, username, password, host="localhost", port=5432
):
    conn = psycopg2.connect(
        host=host,
        port=port,
        database="postgres",
        user=PG_ADMIN,
        password=PG_ADMIN_PASSWORD
    )

    # Create metabase app user with appropriate permissions
    db.drop_db(conn, db_name)
    db.create_user(conn, username, password)
    print(f"Creating metabase db {db_name}")
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(
            sql.SQL(
                "CREATE DATABASE {0} WITH OWNER = {1};"
            ).format(
                sql.Identifier(db_name),
                sql.Identifier(username),
            )
        )
    conn.close()


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
        help="Metabase username to use when connecting to the database server",
        required=True,
    )
    parser.add_argument(
        "-w", "--password",
        help="Metabase user password to use when connecting to the database server",
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

    init_metabase_db(
        args.metabase_db,
        args.username,
        args.password,
        host=args.hostname,
        port=args.port
    )


if __name__ == "__main__":
    cli()

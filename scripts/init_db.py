#!/usr/bin/env python

import psycopg2
from psycopg2 import sql
import argparse


def drop_db(conn, db_name):
    """
    Force drop a database if it exists
    """
    print(f"Dropping database {db_name} if it exists ...")
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(
            sql.SQL(
                "DROP DATABASE IF EXISTS {} WITH (FORCE);"
            ).format(sql.Identifier(db_name))
        )


def create_db(conn, db_name):
    """
    Create a databasee
    """
    print(f"Creating database {db_name} ...")
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(
            sql.SQL(
                "CREATE DATABASE {};"
            ).format(sql.Identifier(db_name))
        )


def init_db(ingest_db, username, password, hostname="localhost", port=5432):
    """
    Drop the db if exists and then create a new db
    Create the ingest user with appropriate permissions
    Create viewer user with appropriate permissions
    """
    # Connect to postgres db
    conn = psycopg2.connect(
        dbname="postgres",
        user=username, password=password, host=hostname, port=port
    )

    # Drop the db if it exists and then create db
    drop_db(conn, ingest_db)
    create_db(conn, ingest_db)


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Initialize the ingest db'
    )
    parser.add_argument(
        "ingest_db",
        help="The name of the database where ingested"
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
        args.ingest_db,
        args.username,
        args.password,
        hostname=args.hostname,
        port=args.port
    )


if __name__ == "__main__":
    cli()

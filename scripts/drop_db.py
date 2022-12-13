#!/usr/bin/env python

import os
import psycopg2
from psycopg2 import sql
import argparse


def drop_db(db_name, username, password, hostname="localhost", port=5432):
    """
    Drop the db if exists
    """
    # Connect to postgres db
    conn = psycopg2.connect(
        dbname="postgres",
        user=username, password=password, host=hostname, port=port
    )

    # Drop the db if it exists and then create db
    print(f"Dropping database {db_name} if it exists ...")
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(
            sql.SQL(
                "DROP DATABASE IF EXISTS {} WITH (FORCE);"
            ).format(sql.Identifier(db_name))
        )


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Drop the db'
    )
    parser.add_argument(
        "db_name",
        help="The name of the database that will be dropped"
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

    drop_db(
        args.db_name,
        args.username,
        args.password,
        hostname=args.hostname,
        port=args.port
    )


if __name__ == "__main__":
    cli()

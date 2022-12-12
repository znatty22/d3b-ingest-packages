#!/usr/bin/env python

import os
import psycopg2
from psycopg2 import sql
import argparse

from config import (
    INGEST_PROCESS_USER,
    INGEST_PROCESS_PASSWORD,
    INGEST_VIEWER_USER,
    INGEST_VIEWER_PASSWORD,
)


def create_schema(conn, schema_name):
    """
    Create schema in db
    """
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(
            sql.SQL(
                "CREATE SCHEMA {0};",
            ).format(
                sql.Identifier(schema_name),
            )
        )


def create_user(conn, user, password):
    """
    Drop db user if it exists
    Create a db user
    """
    with conn.cursor() as cursor:
        conn.autocommit = True
        cursor.execute(
            sql.SQL(
                "DROP USER IF EXISTS {0};"
                "CREATE USER {0} WITH "
                "LOGIN ENCRYPTED PASSWORD {1} "
                "CONNECTION LIMIT 1000;",
            ).format(
                sql.Identifier(user),
                sql.Literal(password)
            )
        )


def grant_privileges(
    conn, ingest_user=INGEST_PROCESS_USER, viewer=INGEST_VIEWER_USER
):
    """
    Grant privileges to user
    """
    with conn.cursor() as cursor:
        conn.autocommit = True
        query = sql.SQL(
            "GRANT CREATE, USAGE ON SCHEMA "
            "{extract_stage}, {transform_stage} TO {ingest_user}, {viewer};"
            "ALTER DEFAULT PRIVILEGES FOR ROLE {ingest_user} IN SCHEMA "
            "{extract_stage}, {transform_stage} "
            "GRANT SELECT ON TABLES TO {viewer};"
        ).format(
            ingest_user=sql.Identifier(ingest_user),
            viewer=sql.Identifier(viewer),
            extract_stage=sql.Identifier("ExtractStage"),
            transform_stage=sql.Identifier("TransformStage"),
        )
        cursor.execute(query)


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
    Create the ingest process user/user
    Create viewer user/user
    """
    # Connect to postgres db
    conn = psycopg2.connect(
        dbname="postgres",
        user=username, password=password, host=hostname, port=port
    )

    # Drop the db if it exists and then create db
    drop_db(conn, ingest_db)
    create_db(conn, ingest_db)

    # Connect to ingest db now
    conn = psycopg2.connect(
        dbname=ingest_db,
        user=username, password=password, host=hostname, port=port
    )
    # Create stage schemas
    for schema_name in ["ExtractStage", "TransformStage"]:
        create_schema(conn, schema_name)

    # Create ingest and viewer users with appropriate permissions
    create_user(conn, INGEST_PROCESS_USER, INGEST_PROCESS_PASSWORD)
    create_user(conn, INGEST_VIEWER_USER, INGEST_VIEWER_PASSWORD)
    grant_privileges(conn)


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

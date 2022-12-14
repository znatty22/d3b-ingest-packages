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
from scripts import db


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


def init_db(ingest_db, username, password, hostname="localhost", port=5432):
    """
    Drop the db if exists and then create a new db
    Create the ingest process user
    Create viewer and ingest user
    """
    # Connect to postgres db
    conn = psycopg2.connect(
        dbname="postgres",
        user=username, password=password, host=hostname, port=port
    )

    # Drop the db if it exists and then create db
    db.drop_db(conn, ingest_db)
    db.create_db(conn, ingest_db)

    # Connect to ingest db now
    conn = psycopg2.connect(
        dbname=ingest_db,
        user=username, password=password, host=hostname, port=port
    )
    # Create stage schemas
    for schema_name in ["ExtractStage", "TransformStage"]:
        db.create_schema(conn, schema_name)

    # Create ingest and viewer users with appropriate permissions
    db.create_user(conn, INGEST_PROCESS_USER, INGEST_PROCESS_PASSWORD)
    db.create_user(conn, INGEST_VIEWER_USER, INGEST_VIEWER_PASSWORD)
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

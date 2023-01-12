#!/usr/bin/env python

import argparse
import os
import time

import sqlalchemy
import pandas

from kf_lib_data_ingest.common.io import read_df
from config import PACKAGES_DIR

from config import (
    INGEST_PROCESS_USER,
    INGEST_PROCESS_PASSWORD,
)

DEFAULT_BATCH_SIZE = 10000


def sanitize_tablename(table_name):
    """
    Remove invalid characters like hyphens
    """
    return "_".join(table_name.split("-"))


def chunked_dataframe_reader(filepath, batch_size=DEFAULT_BATCH_SIZE):
    """
    Read a tabular file into chunks of Dataframes and return a generator
    over those Dataframes
    """
    for i, chunk in enumerate(
        pandas.read_csv(filepath, sep="\t", chunksize=batch_size)
    ):
        yield chunk


def load_table_from_file(
    filepath, schema_name, batch_size, sqla_engine=None, **db_conn_args
):
    """
    Create a table within the specified schema and load it with the data
    from file
    """
    start_time = time.time()

    dispose_at_end = False
    if not sqla_engine:
        print(f"Creating connection to postgres @ {hostname}")
        # Create connection to db
        try:
            username = db_conn_args["username"]
            password = db_conn_args["password"]
            hostname = db_conn_args["hostname"]
            port = db_conn_args["port"]
            db_name = db_conn_args["dbname"]
        except KeyError as e:
            print("Not enough inputs to connect to database!")
            raise
        conn_str = (
            f"postgres://{username}:{password}@{hostname}:{port}/{db_name}"
        )
        sqla_engine = sqlalchemy.create_engine(
            conn_str,
            connect_args={"connect_timeout": 5},
        )
        dispose_at_end = True

    filename = os.path.split(filepath)[-1]
    table_name = sanitize_tablename(os.path.splitext(filename)[0])
    count = 0
    batch_size = DEFAULT_BATCH_SIZE

    # Stream data from file
    print(f"\nLoading file {filename} into db table {table_name}...")
    for i, df in enumerate(
        chunked_dataframe_reader(filepath, batch_size)
    ):
        # Bulk insert rows into db table
        df.to_sql(
            table_name,
            sqla_engine,
            schema=schema_name,
            if_exists="replace",
            index=False,
            method="multi",
            chunksize=batch_size,
        )
        count += df.shape[0]
        print(f"-- Loaded {count} total rows")

    if dispose_at_end:
        eng.dispose()

    elapsed = time.time() - start_time
    elapsed_time_hms = time.strftime('%H:%M:%S', time.gmtime(elapsed))
    print(f"\nElapsed time (hh:mm:ss): {elapsed_time_hms}\n")


def load_db(
    package_path, db_name, username, password, hostname="localhost", port=5432
):
    """
    Load the db with ingest output data from ExtractStage and TransformStage
    User must have permissions to create schema, create tables, insert, delete,
    update tables
    """
    start_time = time.time()

    # Create conn string
    conn_str = (
        f"postgres://{username}:{password}@{hostname}:{port}/{db_name}"
    )
    eng = sqlalchemy.create_engine(
        conn_str,
        connect_args={"connect_timeout": 5},
    )

    # Read tables from disk
    stages = {
        "ExtractStage": "ExtractStage",
        "GuidedTransformStage": "TransformStage"
    }

    # Load tables into db
    for stage_dir, stage_name in stages.items():
        schema_name = stage_name
        data_dir = os.path.join(
            PACKAGES_DIR, package_path, "output", stage_dir
        )
        for filename in os.listdir(data_dir):
            filepath = os.path.join(data_dir, filename)
            if (
                "validation_results" in filepath or
                filename == "metadata.json" or
                filename.startswith(".")
            ):
                print(f"Not a valid ingest file, skipping {filename}")
                continue

            load_table_from_file(
                filepath, schema_name, DEFAULT_BATCH_SIZE, sqla_engine=eng
            )

    eng.dispose()

    elapsed = time.time() - start_time
    elapsed_time_hms = time.strftime('%H:%M:%S', time.gmtime(elapsed))
    print(f"Total elapsed time (hh:mm:ss): {elapsed_time_hms}")


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Initialize the ingest db'
    )
    parser.add_argument(
        "package_path",
        help="The path to the ingest package you want counts for. Path "
        "should be relative to d3b_ingest_packages/packages directory",
    )
    parser.add_argument(
        "db_name",
        help="The name of the database where ingested"
        " data will go",
    )
    parser.add_argument(
        "-u", "--username",
        help="Username of ingest db user",
        required=False,
        default=INGEST_PROCESS_USER
    )
    parser.add_argument(
        "-w", "--password",
        help="Password of ingest db user",
        required=False,
        default=INGEST_PROCESS_PASSWORD
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

    load_db(
        args.package_path,
        args.db_name,
        args.username,
        args.password,
        hostname=args.hostname,
        port=args.port
    )


if __name__ == "__main__":
    cli()

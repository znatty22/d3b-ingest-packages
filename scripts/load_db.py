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
                continue

            print(f"Loading file {filename} into db ...")
            count = 0
            batch_size = DEFAULT_BATCH_SIZE
            for i, df in enumerate(
                chunked_dataframe_reader(filepath, batch_size)
            ):
                table_name = sanitize_tablename(os.path.splitext(filename)[0])
                df.to_sql(
                    table_name,
                    eng,
                    schema=schema_name,
                    if_exists="replace",
                    index=False,
                    method="multi",
                    chunksize=10000,
                )
                count += df.shape[0]
                print(f"-- Loaded {count} total rows")

            elapsed_time = time.time() - start_time
            elapsed_time_hms = time.strftime(
                '%H:%M:%S', time.gmtime(elapsed_time)
            )
            print(f"\nElapsed time (hh:mm:ss): {elapsed_time_hms}\n")

    eng.dispose()

    elapsed = time.time() - start_time
    elapsed_time_hms = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
    print(f"\nTotal elapsed time (hh:mm:ss): {elapsed_time_hms}")


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

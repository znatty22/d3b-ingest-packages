#!/usr/bin/env python

import argparse
import os
from pprint import pprint

import yaml
from yaml.loader import SafeLoader


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
RUN_FILEPATH = os.path.join(ROOT_DIR, "run.yaml")


def generate_db_name(package_path, pull_request_number):
    """
    Generate the name of the ingest database based on the pull request
    number and the package index in the list of packages
    """
    with open(RUN_FILEPATH) as f:
        data = yaml.load(f, Loader=SafeLoader)

    for i, p in enumerate(data['packages']):
        if package_path == p:
            print(f"pr{pull_request_number}_pkg{i}")
            break


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Generate a name for the ingest db based on the PR and '
        'package index in the list of packages'
    )
    parser.add_argument(
        "package_path",
        help="The path to the ingest package you want counts for. Path "
        "should be relative to d3b_ingest_packages/packages directory",
    )
    parser.add_argument(
        "pull_request_number",
        help="The pull request index",
    )
    args = parser.parse_args()

    generate_db_name(args.package_path, args.pull_request_number)


if __name__ == "__main__":
    cli()

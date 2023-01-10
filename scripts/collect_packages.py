#!/usr/bin/env python

import os
import json

import yaml
from yaml.loader import SafeLoader


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
RUN_FILEPATH = os.path.join(ROOT_DIR, "run.yaml")
PACKAGES_DIR = "d3b_ingest_packages/packages"


def get_package():
    """
    Read relative ingest package path from run.yaml
    Check to make sure the path exists
    Output package path
    """

    with open(RUN_FILEPATH) as f:
        data = yaml.load(f, Loader=SafeLoader)

        rel_path = data["package"]
        new_path = os.path.join(PACKAGES_DIR, rel_path)
        # Check if path exists
        os.stat(new_path)
        # write relative ingest package path to stdout
        print(rel_path)


if __name__ == "__main__":
    get_package()

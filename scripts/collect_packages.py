#!/usr/bin/env python

import os
import json

import yaml
from yaml.loader import SafeLoader


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
RUN_FILEPATH = os.path.join(ROOT_DIR, "ci_input.yaml")
PACKAGES_DIR = "d3b_ingest_packages/packages"


def collect_packages():
    """
    Read relative ingest package paths from run.yaml
    Check to make sure each path exists
    Output list of package paths
    """
    pass

    with open(RUN_FILEPATH) as f:
        data = yaml.load(f, Loader=SafeLoader)

        paths = []
        for p in data["packages"]:
            new_path = os.path.join(PACKAGES_DIR, p)
            # Check if path exists
            os.stat(new_path)
            # Write relative ingest package path to stdout
            paths.append(p)
        print(json.dumps(paths))


if __name__ == "__main__":
    collect_packages()

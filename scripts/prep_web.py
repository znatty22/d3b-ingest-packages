#!/usr/bin/env python

import os
import argparse
import shutil

from config import ROOT_DIR, PACKAGES_DIR

template = """
# 🚦 Validation Reports

This site is a central place for you to view the validation results for the
ingest package you're developing in your [Pull Request]({pull_request_url}).

Each time you push a commit to your PR, the Github workflow will do the following:

1. Kick off a dry run ingest (`kidsfirst test <path/to/your/package>`)
2. Run validation on the output data from both the Extract Stage and Transform
   Stage of your ingest
3. Build a validation report for each stage's output data

You can view those validation reports below

## {package_path}

- [ExtractStage Report](results/ExtractStage/validation_results.md)
- [TransformStage Report](results/TransformStage/validation_results.md)
"""


def prep(package_path, pull_request_url):
    """
    Prep the files needed to build the validation report website for the
    ingest package stored at __package_path__

    Fill in a template for the home page of the validation reports site for
    a particular ingest package

    Copy generated validation report files into the website source dir
    """
    print("🗃 Preparing validation website files ...")

    # Fill in the markdown template for the homepage
    index_md = template.format(
        package_path=package_path, pull_request_url=pull_request_url
    )
    with open(os.path.join(ROOT_DIR, "web/docs/index.md"), "w") as index_md_file:
        index_md_file.write(index_md)

    # Copy the validation report files from the ingest run output to the web
    # directory
    stages = {
        "ExtractStage": "ExtractStage",
        "GuidedTransformStage": "TransformStage"
    }
    for stage_name, dest_name in stages.items():
        os.makedirs(
            os.path.join(ROOT_DIR, "web/docs/results", dest_name),
            exist_ok=True
        )
        src = os.path.join(
            PACKAGES_DIR, package_path, "output", stage_name,
            "validation_results", "validation_results.md"
        )
        dst = os.path.join(
            "web/docs/results", dest_name, "validation_results.md"
        )
        print(f"\nCopy {src} to {dst}")

        shutil.copyfile(src, dst)


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Fill in the index.md template for the validation report '
        'site'
    )
    parser.add_argument(
        "package_path",
        help="The path to the ingest package for which the validation report "
        "site will be built. Path should be relative to "
        "d3b_ingest_packages/packages directory",
    )
    parser.add_argument(
        "pull_request_url",
        help="URL to pull request",
    )
    args = parser.parse_args()

    prep(args.package_path, args.pull_request_url)


if __name__ == "__main__":
    cli()

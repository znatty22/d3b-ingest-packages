#!/usr/bin/env python

import os
import argparse
import json
from pprint import pprint

from config import PACKAGES_DIR
from kf_lib_data_ingest.common.concept_schema import CONCEPT
from kf_lib_data_ingest.common.io import read_json, read_df
from kf_lib_data_ingest.validation.reporting.markdown import (
    MarkdownReportBuilder
)


def to_markdown(counts):
    """
    Convert dict to markdown formatted text
    """
    output = []
    builder = MarkdownReportBuilder()
    extract = builder._counts_md({"counts": counts["Extract Stage"]})
    transform = builder._counts_md({"counts": counts["Transform Stage"]})

    output.append("## Summary\n")
    output.append("### Extract Stage\n")
    output.append(extract)
    output.append("\n")
    output.append("### Transform Stage\n")
    output.append(transform)
    output.append("\n")

    return "\n".join(output)


def count_df(df, columns):
    """
    Return unique row count. Uniqueness is determined by columns
    """
    cols = [c for c in list(columns) if c in set(df.columns)]
    if cols:
        return df[cols].drop_duplicates().shape[0]
    else:
        return 0


def counts(package_path):
    """
    Collect unique counts for ID columns in the extract and transform
    stage output
    """
    dirpaths = {
        "Extract Stage": "output/ExtractStage",
        "Transform Stage": "output/GuidedTransformStage",
    }
    columns = {
        "👤 Participant": [CONCEPT.PARTICIPANT.ID],
        "🧪 Biospecimen": [CONCEPT.BIOSPECIMEN.ID],
        "🗂  Genomic File": [CONCEPT.GENOMIC_FILE.ID],
        "🧬 Sequencing Experiment": [CONCEPT.SEQUENCING.ID],
        "🩺 Phenotype": [
            CONCEPT.PARTICIPANT.ID,
            CONCEPT.PHENOTYPE.NAME,
            CONCEPT.PHENOTYPE.EVENT_AGE_DAYS
        ],
        "🚑 Diagnosis": [
            CONCEPT.PARTICIPANT.ID,
            CONCEPT.DIAGNOSIS.NAME,
            CONCEPT.DIAGNOSIS.EVENT_AGE_DAYS
        ],
    }
    counts = {}
    for stage_name, stage_output_dir in dirpaths.items():

        dirpath = os.path.join(PACKAGES_DIR, package_path, stage_output_dir)

        if not os.path.exists(dirpath):
            print(f"Skipping {stage_output_dir} no data exists")
            continue

        print(f"Collecting counts for {stage_name} in {stage_output_dir}")
        counts[stage_name] = {}

        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            if "validation_results" in filepath or filename == "metadata.json":
                continue
            print(f"Counting entities in {filename}")
            df = read_df(filepath)
            for entity, cols in columns.items():
                counts[stage_name][entity] = count_df(df, cols)
    pprint(counts)
    return counts


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Generate entity counts'
    )
    parser.add_argument(
        "package_path",
        help="The path to the ingest package you want counts for. Path "
        "should be relative to d3b_ingest_packages/packages directory",
    )
    args = parser.parse_args()

    results = counts(args.package_path)
    filepath = os.path.join(PACKAGES_DIR, args.package_path, "ci_results.txt")
    with open(filepath, "w") as results_file:
        md = to_markdown(results)
        results_file.write(md)

    print(f"Wrote results to {filepath}")


if __name__ == "__main__":
    cli()

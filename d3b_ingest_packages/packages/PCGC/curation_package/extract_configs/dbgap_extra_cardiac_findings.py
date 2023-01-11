"""
Extract config for extra cardiac findings in a tabular file

The source data csv was generated from surveys here:
https://benchtobassinet.com/wp-content/uploads/2017/11/CHD_GENES_F105CongenitalExtracardiac.pdf

See docstring for ..shared_operations for details on data processing
"""
from kf_lib_data_ingest.etl.extract.operations import *
from d3b_ingest_packages.packages.PCGC.curation_package.shared_operations import (
    extra_cardiac_findings
)
import os

host = 'https://kf-study-creator.kidsfirstdrc.org'
kfid = 'SF_S55HDD41'
source_data_url = f'{host}/download/study/SD_PREASA7S/file/{kfid}'


def do_after_read(df):
    """
    This function will be called before performing the mapping operations list.
    """
    return extra_cardiac_findings.preprocess(df)


operations = extra_cardiac_findings.operations + [
    constant_map(
        m=os.path.basename(__file__),
        out_col="EXTRACT_CONFIG_NAME"
    ),
    constant_map(
        m=kfid,
        out_col="DATA_TRACKER_FILE_ID"
    ),

]

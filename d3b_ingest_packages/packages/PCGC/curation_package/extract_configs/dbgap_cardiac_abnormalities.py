"""
Extract config for cardiac abnormalities in a tabular file

The source data csv was generated from this survey here
https://benchtobassinet.com/wp-content/uploads/2017/11/CHD_GENES_F106CardiacDiagnosis.pdf

See docstring for ..shared_operations for details on data processing
"""

from kf_lib_data_ingest.etl.extract.operations import *
from d3b_ingest_packages.packages.PCGC.curation_package.shared_operations import (
    cardiac_abnormalities
)
import os

host = 'https://kf-study-creator.kidsfirstdrc.org'
kfid = 'SF_X3E4RT7V'
source_data_url = f'{host}/download/study/SD_PREASA7S/file/{kfid}'


def do_after_read(df):
    """
    This function will be called before performing the mapping operations list.
    """
    return cardiac_abnormalities.preprocess(df)


operations = cardiac_abnormalities.operations + [
    constant_map(
        m=os.path.basename(__file__),
        out_col="EXTRACT_CONFIG_NAME"
    ),
    constant_map(
        m=kfid,
        out_col="DATA_TRACKER_FILE_ID"
    ),

]

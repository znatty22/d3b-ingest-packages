"""
Extract config for karyotype abnormalities in PCGC/KING subcohort of INCLUDE
"""

import os

from kf_lib_data_ingest.etl.extract.operations import *
from d3b_ingest_packages.packages.PCGC.curation_package.shared_operations import (
    karyotype_abnormalities
)


host = 'https://kf-study-creator.kidsfirstdrc.org'
kfid = 'SF_DHWW098D'
source_data_url = f'{host}/download/study/SD_Z6MWD3H0/file/{kfid}'

operations = karyotype_abnormalities.operations + [
    constant_map(
        m=os.path.basename(__file__),
        out_col="EXTRACT_CONFIG_NAME"
    ),
    constant_map(
        m=kfid,
        out_col="DATA_TRACKER_FILE_ID"
    ),
]

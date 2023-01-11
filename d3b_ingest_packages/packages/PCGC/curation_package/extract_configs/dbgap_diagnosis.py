"""
Extract config for dbgap diagnoses PCGC 
"""


from d3b_ingest_packages.packages.PCGC.curation_package.shared_operations import (
    patient_diagnosis
)
from kf_lib_data_ingest.etl.extract.operations import *
from kf_lib_data_ingest.common.concept_schema import (
    CONCEPT
)
from kf_lib_data_ingest.common import constants
import os

host = 'https://kf-study-creator.kidsfirstdrc.org'
kfid = 'SF_21BH8AGM'
source_data_url = f'{host}/download/study/SD_PREASA7S/file/{kfid}'

operations = patient_diagnosis.operations + [
    constant_map(
        m=os.path.basename(__file__),
        out_col="EXTRACT_CONFIG_NAME"
    ),
    constant_map(
        m=kfid,
        out_col="DATA_TRACKER_FILE_ID"
    ),
]

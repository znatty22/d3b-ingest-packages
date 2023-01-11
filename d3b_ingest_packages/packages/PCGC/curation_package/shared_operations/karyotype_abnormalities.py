"""
Shared operations to prepare karyotype abnormalities tabular file for
curation
"""

from kf_lib_data_ingest.common import constants
from kf_lib_data_ingest.common.concept_schema import CONCEPT
from kf_lib_data_ingest.etl.extract.operations import *


operations = [
    keep_map(
        in_col="SUBJID",
        out_col=CONCEPT.PARTICIPANT.ID
    ),
    keep_map(
        in_col="ABNORMALITY",
        out_col="SOURCE_CONDITION_TERM"
    ),
    constant_map(
        m=constants.PHENOTYPE.OBSERVED.YES,
        out_col="SOURCE_CONDITION_FREE_TEXT"
    ),
    constant_map(
        m=constants.PHENOTYPE.OBSERVED.YES,
        out_col=CONCEPT.PHENOTYPE.OBSERVED
    ),
    # TODO: Confirm if we want to report ages as NA or use ages from other files.
    constant_map(
        m=constants.COMMON.NOT_REPORTED,
        out_col=CONCEPT.PHENOTYPE.EVENT_AGE_DAYS
    )
]

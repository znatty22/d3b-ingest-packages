"""
Shared operations to prepare cardiac abnormalities tabular file for 
curation
"""
import pandas

from kf_lib_data_ingest.common import constants
from kf_lib_data_ingest.common.concept_schema import CONCEPT
from kf_lib_data_ingest.etl.extract.operations import *


def observed(x):
    """
    Map source observed values to the standard phenotype observed values
    as defined in the mapping rules above
    """
    if x in {'Yes', True, "True", "Abnormal"}:
        return constants.PHENOTYPE.OBSERVED.YES
    elif pandas.isnull(x) or (x in {'No', 'None', False, "False", "Normal"}):
        return constants.PHENOTYPE.OBSERVED.NO
    elif x in {'Unknown'}:
        return constants.COMMON.UNKNOWN
    else:
        return constants.PHENOTYPE.OBSERVED.YES


def preprocess(df):
    """
    This function will be called before performing the mapping operations list.
    """
    phenotype_cols = [
        c for c in df.columns
        if c not in {"SUBJID", "AGE_REPORTED"}
    ]

    # Transpose the file
    df_phenotype = pandas.melt(
        df,
        id_vars=["SUBJID", "AGE_REPORTED"],
        value_vars=phenotype_cols,
        var_name="SOURCE_COLUMN_NAME",
        value_name="SOURCE_COLUMN_VALUE"
    ).drop_duplicates()

    df_phenotype["OBSERVED"] = df_phenotype["SOURCE_COLUMN_NAME"].apply(
        observed)

    return df_phenotype


operations = [
    keep_map(
        in_col="SUBJID",
        out_col=CONCEPT.PARTICIPANT.ID
    ),
    keep_map(
        in_col="SOURCE_COLUMN_NAME",
        out_col="SOURCE_CONDITION_TERM"
    ),
    keep_map(
        in_col="SOURCE_COLUMN_VALUE",
        out_col="SOURCE_CONDITION_FREE_TEXT"
    ),
    keep_map(
        in_col="OBSERVED",
        out_col=CONCEPT.PHENOTYPE.OBSERVED
    ),
    value_map(
        in_col="AGE_REPORTED",
        m=lambda x: int(float(x) * 365.25),
        out_col=CONCEPT.PHENOTYPE.EVENT_AGE_DAYS
    ),
]

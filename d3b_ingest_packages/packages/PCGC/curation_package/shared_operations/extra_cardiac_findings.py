"""
Shared operations to prepare extra cardiac findings tabular file for 
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
    if x in {'Yes'}:
        return constants.PHENOTYPE.OBSERVED.YES
    elif pandas.isnull(x) or (x in {'No', 'None'}):
        return constants.PHENOTYPE.OBSERVED.NO
    elif x in {'Unknown', 'No/Not checked'}:
        return constants.COMMON.UNKNOWN
    elif x in {'Not applicable'}:
        return constants.COMMON.NOT_APPLICABLE
    else:
        return constants.PHENOTYPE.OBSERVED.YES


def preprocess(df):
    """
    This function will be called before performing the mapping operations list.
    """
    # Exclude age columns and numeric columns (e.g. age, height, weight)
    age_columns = [
        c for c in df.columns
        if c.startswith("AGE") or c.endswith("AGE")
    ]
    numeric_columns = [
        c for c in df.columns
        if any(w in c for w in ["HEIGHT", "WEIGHT", "SUBJID"])
    ]
    excluded_cols = set(age_columns + numeric_columns)

    phenotype_cols = [
        c for c in df.columns if c not in excluded_cols
    ]

    # Transpose the file
    df_phenotype = pandas.melt(
        df,
        id_vars=["SUBJID", "AGE_AT_FORM_COMPLETION"],
        value_vars=phenotype_cols,
        var_name="SOURCE_COLUMN_NAME",
        value_name="SOURCE_COLUMN_VALUE"
    ).drop_duplicates()

    df_phenotype["OBSERVED"] = df_phenotype["SOURCE_COLUMN_VALUE"].apply(
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
        in_col="AGE_AT_FORM_COMPLETION",
        m=lambda x: int(float(x) * 365.25),
        out_col=CONCEPT.PHENOTYPE.EVENT_AGE_DAYS
    ),
]

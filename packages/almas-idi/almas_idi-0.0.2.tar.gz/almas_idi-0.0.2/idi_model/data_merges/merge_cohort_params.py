from idi_model.abstracted_packages import furtheredge_pandas as pd


def merge_cohort_parameters(
    sub_df,
    cohort_parameters,
):

    sub_df = pd.merge(
        sub_df, cohort_parameters, on="Cohort", how="left", validate="m:1"
    )
    return sub_df

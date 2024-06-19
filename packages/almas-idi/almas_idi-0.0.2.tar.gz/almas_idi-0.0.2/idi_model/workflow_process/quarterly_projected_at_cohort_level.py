from idi_model.abstracted_packages import furtheredge_pandas as pd
from idi_model.abstracted_packages import furtheredge_numpy as np

from idi_model._1_input_data_manager.data_aggregate import (
    aggregate_projected_quarterly_cohort_level,
)


def quarterly_projected_cohort_level(
    df_monthly_policy_level, list_projected_columns_final
):

    resulted_df_quarter_cohort_level = (
        aggregate_projected_quarterly_cohort_level(
            df_monthly_policy_level,
            ["Cohort", "proj_year", "quarter_proj_index"],
            list_projected_columns_final,
        )
    )

    return resulted_df_quarter_cohort_level

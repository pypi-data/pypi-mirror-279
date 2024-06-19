from idi_model.abstracted_packages import furtheredge_pandas as pd
from idi_model.abstracted_packages import furtheredge_numpy as np

from idi_model.tools.df_tools.extract_infos import extract_quarter_year
from idi_model._1_input_data_manager.data_aggregate import (
    aggregate_projected_quarterly_policy_level,
)


def quarterly_projected_policy_level(
    df_monthly_policy_level, list_projected_columns_final
):

    df_monthly_policy_level = extract_quarter_year(
        df_monthly_policy_level,
        "Proj_Month",
        "proj_year",
        "quarter_proj_index",
    )

    # Aggregating to Quarterly projection at Policy Level

    resulted_df_quarter_policy_level = (
        aggregate_projected_quarterly_policy_level(
            df_monthly_policy_level,
            ["policy_no_", "proj_year", "quarter_proj_index"],
            list_projected_columns_final,
        )
    )

    return resulted_df_quarter_policy_level

from idi_model.abstracted_packages import furtheredge_pandas as pd
from idi_model.abstracted_packages import furtheredge_numpy as np
from idi_model.tools.df_tools.clean_dfs_columns import remove_spaces
from idi_model.tools.df_tools.extract_infos import extract_cohort
from idi_model._1_input_data_manager.data_aggregate import (
    aggregatesum_aggregate_by_pivot,
)
from idi_model._1_input_data_manager.projection import (
    add_projected_months,
)


def process_data(
    df_premium_at_transaction_lvl,
    pivot_variables,
    aggr_variables,
    columns_keep_df,
    values_policy_status,
):

    df_premium_at_transaction_lvl.columns = (
        df_premium_at_transaction_lvl.columns.map(remove_spaces)
    )
    df_premium_at_transaction_lvl.loc[:, "Cohort"] = (
        df_premium_at_transaction_lvl["issue_date"].apply(extract_cohort)
    )

    deposit_premium_at_policy_lvl = aggregatesum_aggregate_by_pivot(
        df_premium_at_transaction_lvl, pivot_variables, aggr_variables
    )
    df_with_keeped_columns = add_projected_months(
        deposit_premium_at_policy_lvl,
        columns_keep_df,
        start="31/12/2020",
        periods=229,
    )

    df_with_keeped_columns["Proj_Month_shifted"] = df_with_keeped_columns[
        "Proj_Month"
    ].shift(1)
    conditions = [
        (
            df_with_keeped_columns["Proj_Month"]
            < df_with_keeped_columns["issue_date"]
        ),
        (
            df_with_keeped_columns["Proj_Month_shifted"]
            < df_with_keeped_columns["inception_date"]
        ),
        (
            df_with_keeped_columns["Proj_Month_shifted"]
            <= df_with_keeped_columns["date_of_expiry"]
        ),
        (
            df_with_keeped_columns["Proj_Month"]
            >= df_with_keeped_columns["date_of_expiry"]
        ),
    ]
    # conditions = [
    #     (df_with_keeped_columns["Proj_Month"] < df_with_keeped_columns["issue_date"]),
    #     (
    #         (
    #             df_with_keeped_columns["Proj_Month"]
    #             <= df_with_keeped_columns["inception_date"]
    #         )
    #         | (df_with_keeped_columns["different_period"].dt.days <= 31)
    #     ),
    #     (
    #         df_with_keeped_columns["Proj_Month"]
    #         <= df_with_keeped_columns["date_of_expiry"]
    #     ),
    #     (
    #         df_with_keeped_columns["Proj_Month"]
    #         > df_with_keeped_columns["date_of_expiry"]
    #     ),
    # ]

    df_with_keeped_columns["policy_status"] = np.select(
        conditions, values_policy_status
    )
    return df_with_keeped_columns

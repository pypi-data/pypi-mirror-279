from idi_model.workflow_process.monthly_projected_at_policy_level import (
    monthly_projected_policy_level,
)

from idi_model.workflow_process.quarterly_projected_at_policy_level import (
    quarterly_projected_policy_level,
)

from idi_model.workflow_process.quarterly_projected_at_cohort_level import (
    quarterly_projected_cohort_level,
)
from idi_model.abstracted_packages import furtheredge_pandas as pd
from idi_model.workflow_process.concat_data import concat_all_dfs, split_data


def full_idi_workflow(
    deposit_df: pd.DataFrame,
    activation_df: pd.DataFrame,
    cohort_df: pd.DataFrame,
    monthly_loss_ratio_df: pd.DataFrame,
    config: dict,
):
    deposit_df["activation_status"] = False
    activation_df["activation_status"] = True

    combined_deposit_activation_df = concat_all_dfs(
        activation_df,
        deposit_df,
        config["keys_df_mapping_deposit"],
        config["keys_df_mapping_activation"],
        None,
    )

    deposit_data, activation_data = split_data(combined_deposit_activation_df)

    df_monthly_policy_level, df_monthly_policy_level_not_projected = (
        monthly_projected_policy_level(
            deposit_data,
            cohort_df,
            monthly_loss_ratio_df,
            config["list_projected_columns"],
            config["list_non_projected_columns"],
            config["pivot_variables"],
            config["agg_variables"],
            config["columns_keep_df_deposit"],
            config["values_policy_status"],
            config["run_settings"],
            "deposit",
            chunk_size=1000,
            return_projected_df=True,
            return_non_projected_df=True,
            write_projected_to_csv=False,
            write_non_projected_to_csv=False,
            projected_csv_path=None,
            non_projected_csv_path=None,
        )
    )

    (
        df_monthly_policy_level_activation,
        df_monthly_policy_level_not_projected_activation,
    ) = monthly_projected_policy_level(
        activation_data,
        cohort_df,
        monthly_loss_ratio_df,
        config["list_projected_columns"],
        config["list_non_projected_columns"],
        config["pivot_variables"],
        config["agg_variables"],
        config["columns_keep_df_activation"],
        config["values_policy_status"],
        config["run_settings"],
        "activation",
        chunk_size=1000,
        return_projected_df=True,
        return_non_projected_df=True,
        write_projected_to_csv=False,
        write_non_projected_to_csv=False,
        projected_csv_path=None,
        non_projected_csv_path=None,
    )

    df_monthly_policy_level = pd.concat(
        [
            df_monthly_policy_level,
            df_monthly_policy_level_activation,
        ],
        ignore_index=True,
    )

    df_monthly_policy_level_not_projected = pd.concat(
        [
            df_monthly_policy_level_not_projected,
            df_monthly_policy_level_not_projected_activation,
        ],
        ignore_index=True,
    )

    list_projected_columns_final = config["list_projected_columns_final"]

    df_quarterly_policy_level = quarterly_projected_policy_level(
        df_monthly_policy_level, list_projected_columns_final
    )

    df_quarterly_cohort_level = quarterly_projected_cohort_level(
        df_monthly_policy_level, list_projected_columns_final
    )

    return (
        df_monthly_policy_level,
        df_monthly_policy_level_not_projected,
        df_quarterly_policy_level,
        df_quarterly_cohort_level,
    )

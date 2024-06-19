from idi_model.abstracted_packages import furtheredge_pandas as pd

from idi_model._1_input_data_manager.data_manipulation import process_data
from idi_model.idi_monthly_model_policy_level import (
    idi_monthly_model_policy_level_deposit,
    idi_monthly_model_policy_level_activation,
)
from idi_model.data_merges.merge_cohort_params import merge_cohort_parameters
from idi_model.tools.df_tools.clean_dfs_columns import (
    drop_duplicates_and_reset_index,
)
import os


def monthly_projected_policy_level(
    df_premium_at_transaction_lvl,
    cohort_parameters_data,
    monthly_loss_ratio_df,
    list_projected_columns,
    list_non_projected_columns,
    pivot_variables,
    aggr_variables,
    columns_keep_df,
    values_policy_status,
    run_settings,
    run_status,
    chunk_size=1000,
    return_projected_df=True,
    return_non_projected_df=True,
    write_projected_to_csv=False,
    write_non_projected_to_csv=False,
    projected_csv_path="reports/ProjResults.csv",
    non_projected_csv_path="reports/NonProjResults.csv",
):
    if run_status == "deposit" and not (df_premium_at_transaction_lvl.empty):
        result_df_projected, result_df_non_projected = (
            monthly_projected_policy_level_deposit(
                df_premium_at_transaction_lvl,
                cohort_parameters_data,
                monthly_loss_ratio_df,
                list_projected_columns,
                list_non_projected_columns,
                pivot_variables,
                aggr_variables,
                columns_keep_df,
                values_policy_status,
                run_settings,
                chunk_size,
                return_projected_df,
                return_non_projected_df,
                write_projected_to_csv,
                write_non_projected_to_csv,
                projected_csv_path,
                non_projected_csv_path,
            )
        )
        return result_df_projected, result_df_non_projected
    elif run_status == "activation" and not (
        df_premium_at_transaction_lvl.empty
    ):
        result_df_projected, result_df_non_projected = (
            monthly_projected_policy_level_after_activation(
                df_premium_at_transaction_lvl,
                cohort_parameters_data,
                monthly_loss_ratio_df,
                list_projected_columns,
                list_non_projected_columns,
                pivot_variables,
                aggr_variables,
                columns_keep_df,
                values_policy_status,
                run_settings,
                chunk_size,
                return_projected_df,
                return_non_projected_df,
                write_projected_to_csv,
                write_non_projected_to_csv,
                projected_csv_path,
                non_projected_csv_path,
            )
        )
        return result_df_projected, result_df_non_projected
    else:
        result_df_projected = None
        result_df_non_projected = None

        return result_df_projected, result_df_non_projected


def monthly_projected_policy_level_deposit(
    df_premium_deposit_at_transaction_lvl,
    cohort_parameters_data,
    monthly_loss_ratio_df,
    list_projected_columns,
    list_non_projected_columns,
    pivot_variables,
    agg_variables,
    columns_keep_df_deposit,
    values_policy_status,
    run_settings,
    chunk_size=1000,
    return_projected_df=True,
    return_non_projected_df=True,
    write_projected_to_csv=False,
    write_non_projected_to_csv=False,
    projected_csv_path="reports/ProjResults.csv",
    non_projected_csv_path="reports/NonProjResults.csv",
):

    if write_projected_to_csv and os.path.exists(projected_csv_path):
        os.remove(projected_csv_path)
    if write_non_projected_to_csv and os.path.exists(non_projected_csv_path):
        os.remove(non_projected_csv_path)
    unique_policy_nos = df_premium_deposit_at_transaction_lvl[
        "policy_no_"
    ].unique()
    counter = 0

    policy_no_chunks = [
        unique_policy_nos[i : i + chunk_size]
        for i in range(0, len(unique_policy_nos), chunk_size)
    ]
    result_df_projected = pd.DataFrame()
    result_df_non_projected = pd.DataFrame()

    for chunk in policy_no_chunks:
        counter = counter + 1
        sub_df = df_premium_deposit_at_transaction_lvl[
            df_premium_deposit_at_transaction_lvl["policy_no_"].isin(chunk)
        ]
        df_premium_deposit_at_transaction_lvl,
        sub_df = process_data(
            sub_df,
            pivot_variables,
            agg_variables,
            columns_keep_df_deposit,
            values_policy_status,
        )

        sub_df = merge_cohort_parameters(sub_df, cohort_parameters_data)

        sub_df = idi_monthly_model_policy_level_deposit(
            sub_df, monthly_loss_ratio_df, "policy_no_", run_settings
        )

        projected_df = sub_df[list_projected_columns]
        non_projected_df = drop_duplicates_and_reset_index(
            sub_df[list_non_projected_columns]
        )

        if return_projected_df:
            result_df_projected = pd.concat(
                [result_df_projected, projected_df], ignore_index=True
            )

        if return_non_projected_df:
            result_df_non_projected = pd.concat(
                [result_df_non_projected, non_projected_df], ignore_index=True
            )

        if write_projected_to_csv:
            projected_df.to_csv(
                projected_csv_path,
                mode="a",
                header=not os.path.exists(projected_csv_path),
                index=False,
                sep=";",
                decimal=",",
                float_format="%.10f",
            )

        if write_non_projected_to_csv:
            non_projected_df.to_csv(
                non_projected_csv_path,
                mode="a",
                header=not os.path.exists(non_projected_csv_path),
                index=False,
                sep=";",
                decimal=",",
                float_format="%.10f",
            )

    if not return_projected_df:
        result_df_projected = None
    if not return_non_projected_df:
        result_df_non_projected = None

    return result_df_projected, result_df_non_projected


def monthly_projected_policy_level_after_activation(
    df_premium_activation_at_transaction_lvl,
    cohort_parameters_data,
    monthly_loss_ratio_df,
    list_projected_columns,
    list_non_projected_columns,
    pivot_variables,
    aggr_variables_activation,
    columns_keep_df_activation,
    values_policy_status,
    run_settings,
    chunk_size=1000,
    return_projected_df=True,
    return_non_projected_df=True,
    write_projected_to_csv=False,
    write_non_projected_to_csv=False,
    projected_csv_path="reports/ProjResultsAfterActivation.csv",
    non_projected_csv_path="reports/NonProjResultsAfterActivation.csv",
):

    if write_projected_to_csv and os.path.exists(projected_csv_path):
        os.remove(projected_csv_path)
    if write_non_projected_to_csv and os.path.exists(non_projected_csv_path):
        os.remove(non_projected_csv_path)
    unique_policy_nos = df_premium_activation_at_transaction_lvl[
        "policy_no_"
    ].unique()
    counter = 0

    policy_no_chunks = [
        unique_policy_nos[i : i + chunk_size]
        for i in range(0, len(unique_policy_nos), chunk_size)
    ]
    result_df_projected = pd.DataFrame()
    result_df_non_projected = pd.DataFrame()

    for chunk in policy_no_chunks:
        counter = counter + 1
        sub_df = df_premium_activation_at_transaction_lvl[
            df_premium_activation_at_transaction_lvl["policy_no_"].isin(chunk)
        ]

        sub_df = process_data(
            sub_df,
            pivot_variables,
            aggr_variables_activation,
            columns_keep_df_activation,
            values_policy_status,
        )

        sub_df = merge_cohort_parameters(sub_df, cohort_parameters_data)

        sub_df = idi_monthly_model_policy_level_activation(
            sub_df, monthly_loss_ratio_df, "policy_no_", run_settings
        )

        projected_df = sub_df[list_projected_columns]
        non_projected_df = drop_duplicates_and_reset_index(
            sub_df[list_non_projected_columns]
        )

        if return_projected_df:
            result_df_projected = pd.concat(
                [result_df_projected, projected_df], ignore_index=True
            )

        if return_non_projected_df:
            result_df_non_projected = pd.concat(
                [result_df_non_projected, non_projected_df], ignore_index=True
            )

        if write_projected_to_csv:
            projected_df.to_csv(
                projected_csv_path,
                mode="a",
                header=not os.path.exists(projected_csv_path),
                index=False,
                sep=";",
                decimal=",",
                float_format="%.10f",
            )

        if write_non_projected_to_csv:
            non_projected_df.to_csv(
                non_projected_csv_path,
                mode="a",
                header=not os.path.exists(non_projected_csv_path),
                index=False,
                sep=";",
                decimal=",",
                float_format="%.10f",
            )

    if not return_projected_df:
        result_df_projected = None
    if not return_non_projected_df:
        result_df_non_projected = None

    return result_df_projected, result_df_non_projected

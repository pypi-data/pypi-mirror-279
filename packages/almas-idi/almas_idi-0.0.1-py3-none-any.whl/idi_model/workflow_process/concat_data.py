from idi_model.abstracted_packages import furtheredge_pandas as pd


def concat_all_dfs(
    activation_data,
    deposit_data,
    data_mapping_deposit,
    data_mapping_activation,
    path_save_combined_data=None,
):
    activation_columns = list(activation_data.columns)
    deposit_columns = list(deposit_data.columns)
    inv_data_mapping_activation = {
        v: k
        for k, v in data_mapping_activation.items()
        if k not in activation_columns
    }
    inv_data_mapping_deposit = {
        v: k
        for k, v in data_mapping_deposit.items()
        if k not in deposit_columns
    }
    activation_data.rename(columns=inv_data_mapping_activation, inplace=True)
    deposit_data.rename(columns=inv_data_mapping_deposit, inplace=True)
    columns_to_keep = list(data_mapping_activation.keys()) + list(
        data_mapping_deposit.keys()
    )
    columns_to_keep = list(set(columns_to_keep))

    for col in columns_to_keep:
        if col not in activation_data.columns:
            activation_data[col] = pd.NA
        if col not in deposit_data.columns:
            deposit_data[col] = pd.NA

    activation_data = activation_data[columns_to_keep]
    deposit_data = deposit_data[columns_to_keep]
    combined_df = pd.concat([deposit_data, activation_data], ignore_index=True)
    if path_save_combined_data:
        combined_df.to_csv(
            path_save_combined_data,
            index=False,
            sep=";",
            decimal=",",
            float_format="%.10f",
        )
    return combined_df


def split_data(
    combined_df,
    poilicy_id_column_name="policy_no_",
    column_check_status="activation_status",
):
    activation_data = combined_df[combined_df[column_check_status] == True]
    activation_ids = list(set(activation_data[poilicy_id_column_name]))
    filtered_deposit_data = combined_df[
        ~combined_df[poilicy_id_column_name].isin(activation_ids)
    ]
    activation_data = activation_data.reset_index(drop=True)
    filtered_deposit_data = filtered_deposit_data.reset_index(drop=True)
    return filtered_deposit_data, activation_data

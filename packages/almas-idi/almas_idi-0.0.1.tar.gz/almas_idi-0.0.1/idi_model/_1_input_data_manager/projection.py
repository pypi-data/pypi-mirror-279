from idi_model.abstracted_packages import furtheredge_pandas as pd


def add_projected_months(
    df_at_transaction_lvl, columns_keep, start="31/12/2020", periods=229
):

    fin_mois = pd.date_range(start=start, periods=periods, freq="ME")
    df_with_keeped_columns = df_at_transaction_lvl[columns_keep]
    columns_mois = list(fin_mois) * len(df_with_keeped_columns)
    df_with_keeped_columns = pd.concat(
        [df_with_keeped_columns] * periods
    ).sort_index()

    df_with_keeped_columns["Proj_Month"] = columns_mois
    return df_with_keeped_columns

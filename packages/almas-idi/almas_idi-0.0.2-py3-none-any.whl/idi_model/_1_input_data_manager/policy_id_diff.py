from idi_model.abstracted_packages import furtheredge_pandas as pd


def get_policy_id_difference(df1, df2, id_column="policy_no_"):
    if id_column not in df1.columns or id_column not in df2.columns:
        raise ValueError(
            f"Column '{id_column}' must be present in both DataFrames"
        )

    ids_df1 = set(df1[id_column].unique())
    ids_df2 = set(df2[id_column].unique())
    diff_ids = ids_df1 - ids_df2

    return pd.Series(list(diff_ids), name=id_column)

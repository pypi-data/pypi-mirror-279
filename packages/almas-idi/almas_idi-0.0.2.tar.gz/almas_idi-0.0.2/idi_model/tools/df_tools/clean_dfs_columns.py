def remove_spaces(column_name):
    return column_name.strip()


def drop_duplicates_and_reset_index(df, subset=None):
    df_cleaned = df.drop_duplicates(subset=subset)

    df_cleaned.reset_index(drop=True, inplace=True)

    return df_cleaned

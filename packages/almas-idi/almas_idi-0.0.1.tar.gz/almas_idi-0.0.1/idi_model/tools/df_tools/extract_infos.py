dict_month_to_quarter = {
    "1": "1",
    "2": "1",
    "3": "1",
    "4": "2",
    "5": "2",
    "6": "2",
    "7": "3",
    "8": "3",
    "9": "3",
    "10": "4",
    "11": "4",
    "12": "4",
}


def extract_cohort(issue_date):
    year = issue_date.year
    # quarter = (date.month - 1) // 3 + 1
    if year <= 2021:
        year = "2021"
        quarter = "4"
    else:
        quarter = dict_month_to_quarter[str(issue_date.month)]

    return f"IDI_{year}Q{quarter}"


def extract_quarter_year(
    df, column_extract_from, year_column_name, quarter_column_name
):
    df[year_column_name] = df[column_extract_from].dt.year
    df[quarter_column_name] = (df[column_extract_from].dt.month - 1) // 3 + 1
    return df

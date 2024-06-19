from idi_model.abstracted_packages import furtheredge_pandas as pd


def aggregatesum_aggregate_by_pivot(df, pivot_variables, aggr_variables):
    agg_functions = {col: "sum" for col in aggr_variables if col in df.columns}
    other_columns = [
        col
        for col in df.columns
        if col not in pivot_variables + aggr_variables
    ]

    for col in other_columns:
        agg_functions[col] = "first"

    aggregated_df = (
        df.groupby(pivot_variables).agg(agg_functions).reset_index()
    )
    return aggregated_df


def aggregate_policy_status_monthly_to_quarterly(column_values):

    unique_values = set(column_values)

    if unique_values == {"Not Started"}:
        return "Not Started"

    if unique_values == {"Construction"}:
        return "Construction"

    if unique_values == {"Coverage"}:
        return "Coverage"

    if unique_values == {"Expired"}:
        return "Expired"

    elif unique_values == {"Not Started", "Construction"}:
        return "Construction"

    elif unique_values == {"Not Started", "Construction", "Coverage"}:
        return "Coverage"

    elif unique_values == {"Construction", "Coverage"}:
        return "Coverage"

    elif unique_values == {"Coverage", "Expired"}:
        return "Coverage"


def aggregate_projected_quarterly_policy_level(
    df, columns_group_by, columns_to_aggregate
):

    if "policy_status" in columns_to_aggregate:
        columns_to_aggregate.remove("policy_status")
        columns_to_aggregate_sum = columns_to_aggregate[:]
    else:
        columns_to_aggregate_sum = columns_to_aggregate

    grouped_df = df.groupby(columns_group_by, as_index=False).agg(
        {col: "sum" for col in columns_to_aggregate_sum}
    )

    grouped_df["policy_status"] = (
        df.groupby(columns_group_by, sort=False)["policy_status"]
        .apply(aggregate_policy_status_monthly_to_quarterly)
        .values
    )

    return grouped_df


def aggregate_projected_quarterly_cohort_level(
    df, columns_group_by, columns_to_aggregate
):
    grouped_df = df.groupby(columns_group_by, as_index=False)[
        columns_to_aggregate
    ].sum()
    row_counts = (
        df.groupby(columns_group_by).size().reset_index(name="counted_rows")
    )
    result_df = pd.merge(grouped_df, row_counts, on=columns_group_by)

    return result_df

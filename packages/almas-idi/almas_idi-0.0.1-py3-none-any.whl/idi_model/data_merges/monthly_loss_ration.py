from idi_model.abstracted_packages import furtheredge_pandas as pd


def merge_monthly_loss_ratio(df_input):
    monthly_loss_ratio = pd.read_csv(
        "inputs/Input_IDI_Projected_Patterns_Q12024_v22042024.csv", sep=";"
    )
    monthly_loss_ratio["monthly_loss_ratio"] = (
        monthly_loss_ratio["incurred_pattern"] * 60
    ) / 100

    df_input = pd.merge(
        df_input,
        monthly_loss_ratio,
        how="left",
        left_on="Coverage_period_index",
        right_on="cov_month_index",
    )
    return df_input

from idi_model.abstracted_packages import furtheredge_pandas as pd
from idi_model.abstracted_packages import furtheredge_numpy as np


def expenses_commissions_sub_module_calculation(output, run_settings):

    output["premium_refunds"] = premium_refunds(output)

    output["management_expense_payment_pattern"] = (
        management_expense_payment_pattern(
            output,
            run_settings["malath_lead_limit_date"],
            run_settings["first_management_expense_pc"],
        )
    )

    output["claims_expense_payment_pattern"] = claims_expense_payment_pattern(
        output,
        run_settings["malath_lead_limit_date"],
        run_settings["first_management_expense_pc"],
    )

    output["mngt_expense_deposit_30"] = mngt_expense_deposit_30(
        output, run_settings["deposit_premium_rate"]
    )

    output["mngt_expense_balance"] = mngt_expense_balance(
        output, run_settings["activation_premium_rate"]
    )

    output["other_expenses_bank_charges"] = other_expenses_bank_charges(output)

    output["claim_handling"] = claim_handling(output)

    output["total_expenses_and_commissions"] = total_expenses_and_commissions(
        output
    )

    output["projected_expenses_and_commissions"] = (
        projected_expenses_and_commissions(output)
    )

    return output


def premium_refunds(output):

    premium_refunds = (
        -output["premium_collected"] * output["monthly_prob_cancellation"]
    )

    return premium_refunds


def management_expense_payment_pattern(
    output, malath_lead_limit_date, first_management_expense_pc
):

    output["management_expense_payment_index"] = np.where(
        (output["Proj_Month"] < malath_lead_limit_date)
        & (
            (output["policy_status"] == "Construction")
            | (output["policy_status"] == "Coverage")
            | (output["policy_status"] == "Expired")
        ),
        1,
        0,
    )

    max_per_policy = pd.DataFrame(
        output.groupby("policy_no_", as_index=False)[
            "management_expense_payment_index"
        ].sum()
    )
    max_per_policy.rename(
        columns={"management_expense_payment_index": "max_per_policy"},
        inplace=True,
    )

    output = pd.merge(
        output, max_per_policy, on="policy_no_", how="left", validate="m:1"
    )

    output["prev_status"] = output["policy_status"].shift(1)

    output["management_expense_payment_index_2"] = np.where(
        (
            (output["Proj_Month"] < malath_lead_limit_date)
            & (output["policy_status"] == "Construction")
            & (output["prev_status"] == "Not Started")
        ),
        first_management_expense_pc,
        np.where(
            (output["management_expense_payment_index"] != 0),
            (
                (1 - first_management_expense_pc)
                / (output["max_per_policy"] - 1)
            ),
            0,
        ),
    )

    return output["management_expense_payment_index_2"]


def claims_expense_payment_pattern(
    output, malath_lead_limit_date, first_management_expense_pc
):

    output["claims_expense_payment_index"] = np.where(
        (output["Proj_Month"] < malath_lead_limit_date)
        & (
            (output["policy_status"] == "Coverage")
            | (output["policy_status"] == "Expired")
        ),
        1,
        0,
    )

    max_per_policy = pd.DataFrame(
        output.groupby("policy_no_", as_index=False)[
            "claims_expense_payment_index"
        ].sum()
    )
    max_per_policy.rename(
        columns={"claims_expense_payment_index": "max_per_policy_claims"},
        inplace=True,
    )

    output = pd.merge(
        output, max_per_policy, on="policy_no_", how="left", validate="m:1"
    )

    output["prev_status"] = output["policy_status"].shift(1)

    output["claims_expense_payment_index_2"] = np.where(
        (
            (output["Proj_Month"] < malath_lead_limit_date)
            & (output["policy_status"] == "Coverage")
            & (output["prev_status"] == "Construction")
        ),
        first_management_expense_pc,
        np.where(
            (output["claims_expense_payment_index"] != 0),
            (
                (1 - first_management_expense_pc)
                / (output["max_per_policy_claims"] - 1)
            ),
            0,
        ),
    )

    return output["claims_expense_payment_index_2"]


def mngt_expense_deposit_30(output, deposit_premium_rate):
    mngt_expense_deposit_30 = (
        -deposit_premium_rate
        * output["Mgt_Exps_Rt"]
        * output["total_agreed_premium"]
        * output["management_expense_payment_pattern"]
    )

    return mngt_expense_deposit_30


def mngt_expense_balance(output, activation_premium_rate):

    mngt_expense_balance = (
        -activation_premium_rate
        * output["Mgt_Exps_Rt"]
        * output["total_agreed_premium"]
        * output["claims_expense_payment_pattern"]
    )

    return mngt_expense_balance


def other_expenses_bank_charges(output):

    other_expenses_bank_charges = (
        -output["Oth_Exps_Rt"] * output["premium_collected"]
    )

    return other_expenses_bank_charges


def claim_handling(output):

    claim_handling = (
        -output["Estimated_insurance_claims_net_of_survivals"]
        * output["Claims_Exps_Rt"]
    )

    return claim_handling


def total_expenses_and_commissions(output):

    total_expenses_and_commissions = (
        output["mngt_expense_deposit_30"]
        + output["mngt_expense_balance"]
        + output["other_expenses_bank_charges"]
        + output["claim_handling"]
        + output["premium_refunds"]
    )

    return total_expenses_and_commissions


def projected_expenses_and_commissions(output):

    projected_expenses_and_commissions = (
        output["total_expenses_and_commissions"] * output["Survival_Pc"]
    )

    return projected_expenses_and_commissions

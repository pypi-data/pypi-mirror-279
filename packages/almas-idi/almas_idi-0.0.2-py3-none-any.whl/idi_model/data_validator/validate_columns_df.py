calculations_dict_validation = {
    "prev_status": ["policy_status"],
    "premium_payment_pattern": ["policy_status", "prev_status"],
    "premium_collected": ["premium_payment_pattern", "total_agreed_premium"],
    "monthly_prob_cancellation": ["policy_status", "Policy_Cancel_Rt"],
    "cancellation_penalties": [
        "cancellation_penalty_rate",
        "total_agreed_premium",
        "monthly_prob_cancellation",
    ],
    "fees_malath_being_leader": [
        "fees_for_malath_being_leader",
        "total_agreed_premium",
    ],
    "expected_premium_income": [
        "fees_malath_being_leader",
        "cancellation_penalties",
        "premium_collected",
    ],
    "Coverage_period_index": [
        "policy_no_",
        "policy_status",
        "policy_status_shifted",
    ],
    "monthly_loss_ratio": ["incurred_pattern"],
    "Survival_Pc": [
        "policy_no_",
        "policy_status",
        "policy_status_shifted",
        "monthly_prob_cancellation",
    ],
    "Estimated_insurance_claims_gross_of_survivals": [
        "total_agreed_premium",
        "monthly_loss_ratio",
    ],
    "Estimated_insurance_claims_net_of_survivals": [
        "Estimated_insurance_claims_gross_of_survivals",
        "Survival_Pc",
    ],
    "risk_adjustment": [
        "Ra_Rt",
        "Estimated_insurance_claims_net_of_survivals",
    ],
    "premium_refunds": [
        "premium_collected",
        "monthly_prob_cancellation",
    ],
    "management_expense_payment_index": [
        "Proj_Month",
        "malath_lead_limit_date",
        "policy_status",
    ],
    "max_per_policy": [
        "policy_no_",
        "management_expense_payment_index",
    ],
    "management_expense_payment_index_2": [
        "policy_status",
        "prev_status",
        "first_management_expense_pc",
        "management_expense_payment_index",
        "max_per_policy",
    ],
    "claims_expense_payment_index": [
        "Proj_Month",
        "malath_lead_limit_date",
        "policy_status",
    ],
    "claims_expense_payment_index_2": [
        "policy_status",
        "prev_status",
        "first_management_expense_pc",
        "claims_expense_payment_index",
    ],
    "mngt_expense_deposit_30": [
        "deposit_premium_rate",
        "Mgt_Exps_Rt",
        "total_agreed_premium",
        "management_expense_payment_pattern",
    ],
    "mngt_expense_balance": [
        "activation_premium_rate",
        "Mgt_Exps_Rt",
        "total_agreed_premium",
        "claims_expense_payment_index",
    ],
    "other_expenses_bank_charges": [
        "Oth_Exps_Rt",
        "premium_collected",
    ],
    "claim_handling": [
        "Estimated_insurance_claims_net_of_survivals",
        "Claims_Exps_Rt",
    ],
    "total_expenses_and_commissions": [
        "mngt_expense_deposit_30",
        "mngt_expense_balance",
        "other_expenses_bank_charges",
        "claim_handling",
        "premium_refunds",
    ],
    "projected_expenses_and_commissions": [
        "total_expenses_and_commissions",
        "Survival_Pc",
    ],
    "expected_reinsurance_premium": [
        "expected_premium_income",
        "Reinsurance_Pc",
    ],
    "expected_reinsurance_claim_recov_cancel_refunds": [
        "Reinsurance_Pc",
        "Estimated_insurance_claims_net_of_survivals",
        "cancellation_penalties",
    ],
    "reinsurance_commissions_amortisation_deposit_30": [
        "policy_status",
        "reinsurance_commissions_amortisation",
    ],
    "Projected reinsurance commissions (15%) (Deposit 30%)": [
        "deposit_premium_rate",
        "Ceded_Comms_Rt",
        "total_agreed_premium",
        "Reinsurance_Pc",
        "reinsurance_commissions_amortisation_deposit_30",
    ],
    "Projected reinsurance mgt fee (1.45%) (Deposit 30%)": [
        "deposit_premium_rate",
        "Mgt_Re_Exps_Rt",
        "total_agreed_premium",
        "Reinsurance_Pc",
        "reinsurance_commissions_amortisation_deposit_30",
    ],
    "Projected reinsurance commissions (15%) (balance)": [
        "activation_premium_rate",
        "Ceded_Comms_Rt",
        "total_agreed_premium",
        "Reinsurance_Pc",
        "management_expense_payment_pattern",
    ],
    "Projected reinsurance commissions (15%) (Deposit 30%)": [
        "deposit_premium_rate ",
        "Ceded_Comms_Rt",
        "total_agreed_premium",
        "Reinsurance_Pc",
        "management_expense_payment_pattern",
    ],
    "Projected reinsurance commissions (15%) (balance)": [
        "activation_premium_rate",
        "Ceded_Comms_Rt",
        "total_agreed_premium",
        "Reinsurance_Pc",
        "claims_expense_payment_index",
    ],
}


def check_keys_in_df(df, keys):

    return all(key in df.columns for key in keys)


def check_and_search_variables(df, keys):
    missing_keys_check = [key for key in keys if key not in df.columns]
    missing_keys_search = tuple(missing_keys_check)
    all_keys_present = not bool(missing_keys_check)
    return all_keys_present, missing_keys_search

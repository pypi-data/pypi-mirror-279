from idi_model.abstracted_packages import furtheredge_pandas as pd
from idi_model.abstracted_packages import furtheredge_numpy as np

from idi_model._2_undisc_cf_projector._1_premium_deposit import (
    premium_sub_module_calculation,
)
from idi_model._2_undisc_cf_projector._2_lrc_claims_deposit import (
    lrc_claims_sub_module_calculation,
)
from idi_model._2_undisc_cf_projector._3_risk_adjustment_deposit import (
    risk_adjustment_sub_module_calculation,
)
from idi_model._2_undisc_cf_projector._4_expenses_commissions_deposit import (
    expenses_commissions_sub_module_calculation,
)
from idi_model._2_undisc_cf_projector._5_ceeded_cashflows_deposit import (
    ceeded_cashflows_sub_module_calculation,
)
from idi_model._2_undisc_cf_projector._1_premium_activation import (
    premium_sub_module_calculation_activation,
)
from idi_model._2_undisc_cf_projector._4_expenses_commissions_activation import (
    expenses_commissions_sub_module_calculation_activation,
)
from idi_model._2_undisc_cf_projector._5_ceeded_cashflows_activation import (
    ceeded_cashflows_sub_module_calculation_activation,
)


def idi_monthly_model_policy_level_deposit(
    prepared_data, monthly_loss_ratio_df, grouped_by_column_name, run_settings
):

    prepared_data = premium_sub_module_calculation(prepared_data, run_settings)

    prepared_data = lrc_claims_sub_module_calculation(
        prepared_data, monthly_loss_ratio_df, grouped_by_column_name
    )

    prepared_data = risk_adjustment_sub_module_calculation(prepared_data)

    prepared_data = expenses_commissions_sub_module_calculation(
        prepared_data, run_settings
    )

    prepared_data = ceeded_cashflows_sub_module_calculation(
        prepared_data, run_settings
    )

    return prepared_data


def idi_monthly_model_policy_level_activation(
    prepared_data, monthly_loss_ratio_df, grouped_by_column_name, run_settings
):

    prepared_data = premium_sub_module_calculation_activation(
        prepared_data, run_settings
    )

    prepared_data = lrc_claims_sub_module_calculation(
        prepared_data, monthly_loss_ratio_df, grouped_by_column_name
    )

    prepared_data = risk_adjustment_sub_module_calculation(prepared_data)

    prepared_data = expenses_commissions_sub_module_calculation_activation(
        prepared_data, run_settings
    )

    prepared_data = ceeded_cashflows_sub_module_calculation_activation(
        prepared_data, run_settings
    )

    return prepared_data

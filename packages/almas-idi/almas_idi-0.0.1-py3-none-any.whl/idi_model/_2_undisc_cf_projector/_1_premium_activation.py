from idi_model.abstracted_packages import furtheredge_numpy as np
from idi_model._2_undisc_cf_projector._1_premium_deposit import (
    premium_payment_pattern,
    monthly_probability_of_cancellation,
    cancellation_penalties,
    fees_malath_being_leader,
    expected_premium_income,
)


def premium_sub_module_calculation_activation(output, run_settings):

    output["premium_payment_pattern"] = premium_payment_pattern(
        output,
        run_settings["deposit_premium_rate"],
        run_settings["activation_premium_rate"],
    )

    output["premium_collected"] = premium_collected_activation(output)

    output["monthly_prob_cancellation"] = monthly_probability_of_cancellation(
        output
    )

    output["cancellation_penalties"] = cancellation_penalties(
        output, run_settings["cancellation_penalty_rate"]
    )

    output["fees_malath_being_leader"] = fees_malath_being_leader(
        output, run_settings["fees_for_malath_being_leader"]
    )

    output["expected_premium_income"] = expected_premium_income(output)

    return output


def premium_collected_activation(output):

    premium_collected = np.where(
        output["premium_payment_pattern"] == 0.30,
        output["deposit_premium_30%"],
        np.where(
            (output["premium_payment_pattern"] == 0.70),
            output["activation_premium"],
            0,
        ),
    )

    return premium_collected

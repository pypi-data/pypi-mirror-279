from idi_model.abstracted_packages import furtheredge_numpy as np


def premium_sub_module_calculation(output, run_settings):

    output["premium_payment_pattern"] = premium_payment_pattern(
        output,
        run_settings["deposit_premium_rate"],
        run_settings["activation_premium_rate"],
    )

    output["premium_collected"] = premium_collected(output)

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


def premium_payment_pattern(
    output, deposit_premium_rate, activation_premium_rate
):

    output["prev_status"] = output["policy_status"].shift(1)

    premium_payment_pattern = np.where(
        (output["policy_status"] == "Construction")
        & (output["prev_status"] == "Not Started"),
        deposit_premium_rate,
        np.where(
            (output["policy_status"] == "Coverage")
            & (output["prev_status"] == "Construction"),
            activation_premium_rate,
            0,
        ),
    )

    output.drop(["prev_status"], axis=1, inplace=True)

    return premium_payment_pattern


def premium_collected(output):

    premium_collected = (
        output["premium_payment_pattern"] * output["total_agreed_premium"]
    )

    return premium_collected


def monthly_probability_of_cancellation(output):

    monthly_probability_of_cancellation = np.where(
        (output["policy_status"] == "Construction"),
        1 - (1 - output["Policy_Cancel_Rt"]) ** (1 / 12),
        0,
    )

    return monthly_probability_of_cancellation


def cancellation_penalties(output, cancellation_penalty_rate):

    cancellation_penalties = (
        cancellation_penalty_rate
        * output["total_agreed_premium"]
        * output["monthly_prob_cancellation"]
    )

    return cancellation_penalties


def fees_malath_being_leader(output, fees_for_malath_being_leader):

    fees_malath_being_leader = (
        fees_for_malath_being_leader * output["total_agreed_premium"]
    )

    return fees_malath_being_leader


def expected_premium_income(output):

    expected_premium_income = (
        output["fees_malath_being_leader"]
        + output["cancellation_penalties"]
        + output["premium_collected"]
    )

    return expected_premium_income

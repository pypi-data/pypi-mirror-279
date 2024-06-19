def risk_adjustment_sub_module_calculation(output):

    output["risk_adjustment"] = risk_adjustment(output)

    return output


def risk_adjustment(output):

    risk_adjustment = (
        output["Ra_Rt"] * output["Estimated_insurance_claims_net_of_survivals"]
    )

    return risk_adjustment

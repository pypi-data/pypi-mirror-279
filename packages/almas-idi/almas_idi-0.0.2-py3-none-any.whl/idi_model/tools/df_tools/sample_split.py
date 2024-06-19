from idi_model.abstracted_packages import furtheredge_pandas as pd


def sample_one_policy(df, policy_id):
    activation_data = df[df["activation_status"] == True].copy()
    deposit_data = df[df["activation_status"] == False].copy()
    activated_policy_df = activation_data[
        activation_data["policy_no_"] == policy_id
    ]
    deposit_policy_df = deposit_data[deposit_data["policy_no_"] == policy_id]
    list_dfs = [activated_policy_df, deposit_policy_df]
    sample_df = pd.concat(list_dfs)
    return sample_df


def sample_and_cohort_data(df, sample_size=3, policy_id=0):

    activation_data = df[df["activation_status"] == True].copy()
    deposit_data = df[df["activation_status"] == False].copy()
    activated_policy_df = activation_data[
        activation_data["policy_no_"] == policy_id
    ]
    deposit_policy_df = deposit_data[deposit_data["policy_no_"] == policy_id]
    policy_forced = pd.concat([activated_policy_df, deposit_policy_df])

    activation_data["quarter"] = (
        activation_data["issue_date"].dt.to_period("Q").astype(str)
    )
    deposit_data["quarter"] = (
        deposit_data["issue_date"].dt.to_period("Q").astype(str)
    )

    def sample_within_cohorts(data):

        grouped = data.groupby("quarter")
        sampled_data = grouped.apply(
            lambda x: x.sample(n=min(sample_size, len(x)))
        ).reset_index(drop=True)

        return sampled_data

    activation_sample = sample_within_cohorts(activation_data)
    deposit_sample = sample_within_cohorts(deposit_data)
    list_dfs = [activation_sample, deposit_sample]
    if not (policy_forced.empty):
        list_dfs.append(policy_forced)
    else:
        list_dfs.append(policy_forced)
    sample_df = pd.concat(list_dfs)

    return sample_df

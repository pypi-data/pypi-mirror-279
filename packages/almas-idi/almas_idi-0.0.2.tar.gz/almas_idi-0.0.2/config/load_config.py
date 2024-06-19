import json
from datetime import datetime


def load_config(config_file="config/config.json"):
    with open(config_file, "r") as f:
        config = json.load(f)
    return config


def load_config_extrenal(config):
    return config


config = load_config()
config_deposit = load_config("config/config_deposit.json")
config_activation = load_config("config/config_activation.json")
config.update(config_deposit)
config.update(config_activation)

run_settings = config["run_settings"]
run_settings["start_date"] = datetime.strptime(
    run_settings["start_date"], "%d/%m/%Y"
)
run_settings["valuation_date"] = datetime.strptime(
    run_settings["valuation_date"], "%d/%m/%Y"
)
run_settings["malath_lead_limit_date"] = datetime.strptime(
    run_settings["malath_lead_limit_date"], "%d/%m/%Y"
)

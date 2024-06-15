import yaml
from pathlib import Path
from pystacho.helper import Helper


class Config:
    DEFAULT_ADAPTER = 'sqlite'

    def __init__(self):
        if not Path(Helper.config_file()).is_file():
            raise FileNotFoundError(f"Config file not found: {Helper.config_file()}")

        with open(Helper.config_file(), "r") as file:
            self.config = yaml.safe_load(file)

    def database_config(self):
        return self.config["pystacho"]["database"]

    def logging_config(self):
        return self.config["pystacho"]["logging"]

    def adapter_name(self):
        return self.database_config()["adapter"] or self.DEFAULT_ADAPTER

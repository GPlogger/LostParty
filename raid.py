import os
import yaml


class Raid:
    raid_condition_dir = "./raid_conditions"

    def __init__(self, name, minimum_limit_level, maximum_limit_level):
        self.name = name
        self.minimum_limit_level = minimum_limit_level
        self.maximum_limit_level = maximum_limit_level
        self.conditions = []

    def check_limit_level(self, level):
        return self.minimum_limit_level <= level <= self.maximum_limit_level

    def get_limit_level(self):
        pass

    @classmethod
    def load(cls, raid_party_name):
        raid_condition_file_path = os.path.join(cls.raid_condition_dir, raid_party_name + ".yaml")
        with open(raid_condition_file_path, "r") as f:
            raid_conditions = yaml.load(f, Loader=yaml.FullLoader)
        return cls(**raid_conditions)

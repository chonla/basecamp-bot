"""Config

A configuration handler for bot.
"""

import yaml


class Config:
    """Config

    A bot configuration.
    """
    def __init__(self, yaml_file: str = ''):
        """___init___

        A constructor. You can pass yaml_file which is filename or stream reader.
        The yaml configuration will be stored in the object for later uses.
        """
        if yaml_file != '':
            with open(yaml_file, encoding='utf-8') as yaml_str:
                self.load(yaml_str)

    def load(self, yaml_str: str):
        """load

        To load a yaml string for stream reader into internal storage.
        """
        self._config = yaml.safe_load(yaml_str)

    def get(self, key: str, default_value: any = '') -> any:
        """get

        To get configuration value. You can address nested value by using dot (.) as a separator.
        """
        chained_keys = key.split('.')
        current_node = self._config
        for k in chained_keys:
            if k in current_node:
                current_node = current_node[k]
            else:
                return default_value
        return current_node

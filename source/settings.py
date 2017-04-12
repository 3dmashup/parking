import json


def get_settings():
    """
    get_settings  return the configuration  settings from a json file
    :return: settings dictionary
    """
    with open('config/config.json') as data_file:
        settings = json.load(data_file)
    return settings

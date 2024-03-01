import configparser

# Path to the INI file
ini_file_path = "./config.ini"


def get_from_ini(thingToGet):
    config = configparser.ConfigParser()
    config.read(ini_file_path)

    # Get values from the INI file
    result = config.get("Settings", thingToGet)

    return result

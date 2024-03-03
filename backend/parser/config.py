import configparser

config = configparser.ConfigParser()
config.read("config.ini")
config = config["Settings"]

azure_api_key = config["AZURE_OPEN_AI_API_KEY"]
azure_endpoint = config["AZURE_OPENAI_ENDPOINT"]

postgres_connection_string = config["POSTGRES_CONNECTION_STRING"]
postgres_collection_name = config["POSTGRES_COLLECTION_NAME"]

huggingface_model = config["HUGGINGFACE_MODEL"]

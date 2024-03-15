import configparser

config = configparser.ConfigParser()
config.read("config.ini")
config = config["Settings"]

# API STUFF
host = config["HOST"]
port = int(config["PORT"])
reload = config["RELOAD"]


# FILE STUFF
data_directory = config["DATA_DIRECTORY"]
resume_directory = config["RESUME_DIRECTORY"]
info_directory = config["INFO_DIRECTORY"]
info_file_name = config["INFO_CSV_FILE"]

column_names = config["COLUMN_NAMES"].split(",")


# AZURE STUFF
azure_api_key = config["AZURE_OPEN_AI_API_KEY"]
azure_endpoint = config["AZURE_OPENAI_ENDPOINT"]

# POSTGRESQL STUFF
postgresql_connection_string = config["POSTGRESQL_CONNECTION_STRING"]
postgresql_collection_name = config["POSTGRESQL_COLLECTION_NAME"]
raw_postgresql_connection_string = config["RAW_POSTGRESQL_CONNECTION_STRING"]
postgresql_collection_table = config["POSTGRESQL_COLLECTION_TABLE"]
postgresql_embedding_table = config["POSTGRESQL_EMBEDDING_TABLE"]
k_documents = config["NUMBER_OF_DOCUMENTS_TO_RETRIEVE"]

# HUGGING FACE STUFF
huggingface_model = config["HUGGINGFACE_MODEL"]

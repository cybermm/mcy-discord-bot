import json

config_path = 'data/config.json'
string_path = 'data/string.json'

with open(config_path) as config_file, \
     open(string_path) as string_file:
     
    config_json = json.loads(config_file.read())
    string_json = json.loads(string_file.read())

# to get config data
def get_config(key):
    return config_json[key]

# to get string data
def get_string(key):
    return string_json[key]
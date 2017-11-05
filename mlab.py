import mongoengine

# mongodb://<dbuser>:<dbpassword>@ds241395.mlab.com:41395/goficer
host = "ds241395.mlab.com"
port = 41395
db_name = "goficer"
user_name = "admin"
password = "admin"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())

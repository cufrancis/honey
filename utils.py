import json

def body_decode(string):
    """
    解析body_arguments 到json
    """
    if isinstance(string, bytes):
        string = bytes.decode(string)

    if isinstance(string, str):
        # "".join(string.split())
        data = json.loads(string)
    return data

def json_convert(o):
    if isinstance(o, ObjectId):
        return str(o)
    if isinstance(o, datetime.datetime):
        return o.__str__()

# def url(path):
#     return path+

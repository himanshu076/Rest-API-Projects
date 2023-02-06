import json
import requests

ENDPOINT = "http://127.0.0.1:8000/api/status/"


def do(method='get', data={}, is_json=True):
    headers = {}
    if is_json:
        headers['content-type'] = 'application/json'
        data = json.dumps(data)
    r = requests.request(method, ENDPOINT , data=data, headers=headers)
    print(r.text)
    print(r.status_code)
    return r

# do(data={'id':50})
do(method='put',data={'id':5, 'content':'some repeted new content.', 'user':1})
# do(method='post',data={'content':'some repeted new content.', 'user':1})
do(method='delete',data={'id':7})

# r = requests.request("get", "http://127.0.0.1:8000/api/status/?id=" + str(id), data={"id": 12})
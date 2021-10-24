import json

data = json.load(open('member_stack.json', 'r'))

ls = data['877399405056102431']

js = dict()
for item in ls:
    user_id = item['user']['id']
    js["877399405056102431"] = {[str(user_id)]: item}

print(js)
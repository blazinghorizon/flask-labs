from flask import Flask, request

app = Flask(__name__)

user_list: list[str] = []

def list_repr(users: list) -> str:
    if len(users) == 1:
        return users[0]
    
    output: str = users[0]
    for i in range(1, len(users) - 2, 1):
        output += ', '
        output += users[i]
    
    output += f' and {users[-1]}'

    return output

@app.route("/", methods=['GET', 'POST'])
def root():
    name = request.args.get('name', None)

    if request.method == 'GET':
        if len(user_list) == 0:
            return "The room is full of people who care..."
        else:
            return f"There are {list_repr(user_list)} in the room"

    elif request.method == 'POST':
        if name is not None: user_list.append(name)

    return

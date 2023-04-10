from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def root():
    name = request.args.get('name', None)
    return "<p>Hello, World!</p>" if name is None else f"<p>Hello, {name}!</p>"
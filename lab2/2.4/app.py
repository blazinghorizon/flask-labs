from flask import Flask, render_template

app = Flask(__name__)

@app.route('/first')
def first():
    return render_template('1.html')

@app.route('/second')
def second():
    return render_template('2.html')

@app.route('/third')
def third():
    return render_template('3.html')
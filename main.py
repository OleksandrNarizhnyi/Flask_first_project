from flask import Flask


app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/user/<string:username>')
def greeting_user(username):
 return f'Hello, {username}'


if __name__ == "__main__":
    app.run(debug=True)
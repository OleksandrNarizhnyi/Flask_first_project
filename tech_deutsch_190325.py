from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/v1/home')
def home_page():
    return jsonify({"response": "Home Page Content"})

@app.route('/api/v1/<path:filepath>')
def get_file(filepath):
    return jsonify({"response": f"{filepath}"})

if __name__ == '__main__':
    app.run(debug=True)
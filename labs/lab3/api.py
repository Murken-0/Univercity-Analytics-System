from flask import Flask, jsonify, request
from main import go_lab3

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_lab3():
    group = request.args.get('group')
    courses = go_lab3(group)
    return jsonify({'group': group, "courses": courses})

if __name__ == '__main__':
    app.run(debug=True, port=3003)
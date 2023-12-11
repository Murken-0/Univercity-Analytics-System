from flask import Flask, jsonify, request
from main import go_lab1

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_lab1():
    phrase = request.args.get('phrase')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    students = go_lab1(phrase, start_date, end_date)
    dict_students = [{'fullname':st[0], 'code':st[1], 'percent':st[2]} for st in students]

    return jsonify({'students': dict_students})

if __name__ == '__main__':
    app.run(debug=True, port=3001)
from flask import Flask, jsonify, request
from main import go_lab2

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_lab2():
    course = request.args.get('course')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    volumes = go_lab2(course, start_date, end_date)
    dict_volumes = [{'class_title':volumes[0][i], 'date':volumes[1][i], 'pair_number':volumes[2][i], 'volume':volumes[3][i]} for i in range(len(volumes))]
    
    return jsonify({'volumes': dict_volumes})

if __name__ == '__main__':
    app.run(debug=True, port=3002)
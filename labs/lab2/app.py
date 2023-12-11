from flask import Flask, jsonify, request
from queries.neo4j_query import get_class_volumes

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_lab2():
    course = request.args.get('course')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    volumes = go_lab2(course, start_date, end_date)
    dict_volumes = [{'class_title':volumes[0][i], 'date':volumes[1][i], 'pair_number':volumes[2][i], 'volume':volumes[3][i]} for i in range(len(volumes))]
    
    return jsonify({'volumes': dict_volumes})

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(success=True)

def go_lab2(course:str, start_date:str, end_date:str) -> list:
    info = get_class_volumes(course, start_date, end_date)
    if not info[0]:
        raise ValueError('Не найдено занятий по курсу')
    if not info[1]:
        raise ValueError('Не найдено расписание для занятий')
    if not info[2]:
        raise ValueError('Не найдено расписание для занятий')
    if not info[3]:
        raise ValueError('Не найдены студенты')
    return info

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3002)
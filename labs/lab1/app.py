from flask import Flask, jsonify, request
from queries.elastic_query import search_materials
from queries.postgres_query import get_attended_percentage
from queries.redis_query import get_student_data
from queries.neo4j_query import get_students_and_shedule

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_lab1():
    phrase = request.args.get('phrase')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    students = go_lab1(phrase, start_date, end_date)
    dict_students = [{'fullname':st[0], 'code':st[1], 'percent':st[2]} for st in students]

    return jsonify({'students': dict_students})

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(success=True)

def go_lab1(phrase, start_date, end_date):
    classes = search_materials(phrase)
    if not classes:
        raise ValueError('Не найдено занятий с таким термином')
    
    students, schedules = get_students_and_shedule(classes)
    if not students:
        raise ValueError('Не найдены студенты')
    if not schedules:
        raise ValueError('Не найдено расписание')

    students_with_percent = get_attended_percentage(students, schedules, start_date, end_date)
    if not students_with_percent:
        raise ValueError("Ошибка с расчетом процента почещения")
    
    result = []
    for student_info in students_with_percent:
        name, code = get_student_data(student_info[0])
        result.append([name, code, round(student_info[1], 2)])

    return result

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
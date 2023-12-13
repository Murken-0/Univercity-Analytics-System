from flask import Flask, jsonify, request, Response
from functools import wraps
import requests
from queries.elastic_query import search_materials
from queries.postgres_query import get_attended_percentage
from queries.redis_query import get_student_data
from queries.neo4j_query import get_students_and_shedule

app = Flask(__name__)

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token.split(" ")[0] != 'Bearer':
            return jsonify({'message': 'Недействительный токен'}), 401, {'WWW-Authenticate': 'Bearer'}
        
        token = token.split(" ")[1]
        auth_service_url = "http://auth:3000/validate"
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.post(auth_service_url, headers=headers)
        if response.status_code == 200:
            return f(*args, **kwargs)
        else:
            return jsonify({'message': 'Недействительный токен'}), 401, {'WWW-Authenticate': 'Bearer'}

    return decorated_function

@app.route('/', methods=['GET'])
@token_required
def get_lab1():
    phrase = request.args.get('phrase')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        students = go_lab1(phrase, start_date, end_date)
    except ValueError as err:
        return jsonify({"error": str(err)}), 204
    dict_students = [{'fullname':st[0], 'code':st[1], 'percent':st[2]} for st in students]

    return jsonify({'students': dict_students}), 200

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
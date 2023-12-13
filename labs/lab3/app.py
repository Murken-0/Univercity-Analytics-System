from flask import Flask, jsonify, request
from functools import wraps
import requests
from queries.neo4j_query import get_courses_schedules, get_students
from queries.postgres_query import get_students_hours
from queries.redis_query import get_student_data

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
def get_lab3():
    group = request.args.get('group')

    try:
        courses = go_lab3(group)
    except ValueError as err:
        return jsonify({"error": str(err)}), 204
    
    return jsonify({'group': group, "courses": courses}), 200

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(success=True)

def go_lab3(group:str) -> list:
    student_ids = get_students(group)
    if not student_ids:
        raise ValueError("Не найдены студенты")
    
    course_schedules = get_courses_schedules(group)
    if not course_schedules:
        raise ValueError("Не найдено расписание")
    
    courses = []
    for course_item in course_schedules:
        title = course_item[0]
        hours_info = get_students_hours(student_ids, course_item[1])
        planned = hours_info[0][2]
        students = []
        for item in hours_info:
            name, code = get_student_data(item[0])
            students.append({"fullname":name, "code":code, "valid_hours":item[1]})

        courses.append({"title":title, "planned_hours":planned, "students": students})

    return courses

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3003)
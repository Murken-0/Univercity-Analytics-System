from flask import Flask, jsonify, request
from functools import wraps
import requests
from queries.neo4j_query import get_class_volumes

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
def get_lab2():
    course = request.args.get('course')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        volumes = go_lab2(course, start_date, end_date)
    except ValueError as err:
        return jsonify({"error": str(err)}), 204
    dict_volumes = [{'class_title':volumes[0][i], 'date':volumes[1][i], 'pair_number':volumes[2][i], 'volume':volumes[3][i]} for i in range(len(volumes))]
    
    return jsonify({'volumes': dict_volumes}), 200

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
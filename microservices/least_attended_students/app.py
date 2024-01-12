from flask import Flask, jsonify, request
from functools import wraps
import requests
from queries.main import get_least_attended_students

app = Flask(__name__)

def authorized(f):
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
@authorized
def get_lab1():
    phrase = request.args.get('phrase')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        students = get_least_attended_students(phrase, start_date, end_date)
    except ValueError as err:
        return jsonify({"error": str(err)}), 204
    dict_students = [{'fullname':st[0], 'code':st[1], 'percent':st[2]} for st in students]

    return jsonify({'students': dict_students}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
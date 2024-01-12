from flask import Flask, jsonify, request
from functools import wraps
import requests
from queries.main import get_audience_size

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
def get_lab2():
    course = request.args.get('course')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        volumes = get_audience_size(course, start_date, end_date)
    except ValueError as err:
        return jsonify({"error": str(err)}), 204
    dict_volumes = [{'class_title':volumes[0][i], 'date':volumes[1][i], 'pair_number':volumes[2][i], 'volume':volumes[3][i]} for i in range(len(volumes[0]))]
    
    return jsonify({'volumes': dict_volumes}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3002)
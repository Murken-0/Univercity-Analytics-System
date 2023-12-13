from flask import Flask, request, jsonify
import psycopg2
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.update(
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf',
    ISSUER='Murken'
)

conn = psycopg2.connect(
    host="postgres",
    port="5432",
    database="practice",
    user="admin",
    password="admin"
)
cur = conn.cursor()

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Неправильная авторизация'}), 401
    
    hashed_password = generate_password_hash(password, method='pbkdf2', salt_length=16)

    cur.execute(f"SELECT id FROM users WHERE username = '{username}'")
    if cur.fetchone():
        return jsonify({'message': 'Пользователь с таким логином уже существует'}), 401

    cur.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{hashed_password}')")
    conn.commit()
    cur.execute(f"SELECT id FROM users WHERE username = '{username}' AND password = '{hashed_password}'")
    id = cur.fetchall()[0][0]

    exp_time = datetime.utcnow() + timedelta(minutes=30)
    token = jwt.encode({'iss':app.config.get('ISSUER'), 'exp': exp_time}, app.config.get('SECRET_KEY'), algorithm="HS256")
    cur.execute(f"INSERT INTO tokens (user_id, token, expire_at) VALUES ({id}, '{token}', '{exp_time.isoformat()}')")
    conn.commit()

    return jsonify({'token': token}), 200

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if  not username or not password:
        return jsonify({'message': 'Неправильная авторизация'}), 401
    
    cur.execute(f"SELECT id, username, password FROM users WHERE username = '{username}'")
    user = cur.fetchone()

    if not user:
        return jsonify({'message': 'Пользователь с такими данными не найден'}), 401
    
    if check_password_hash(user[2], password):
        exp_time = datetime.utcnow() + timedelta(minutes=30)
        token = jwt.encode({'iss':app.config.get('ISSUER'), 'exp': exp_time}, app.config.get('SECRET_KEY'), algorithm="HS256")
        cur.execute(f"INSERT INTO tokens (user_id, token, expire_at) VALUES ({user[0]}, '{token}', '{exp_time.isoformat()}')")
        conn.commit()
        return jsonify({'token': token}), 200
    
    return jsonify({'message': 'Пользователь с такими данными не найден'}), 401 

@app.route('/validate', methods=['POST'])
def validate_token():
    token = request.headers.get('Authorization')
    if  not token or len(token.split(" ")) != 2:
        return jsonify({'message': 'Неправильная авторизация'}), 401

    token = token.split(" ")[1]

    cur.execute(f"SELECT id FROM tokens WHERE token = '{token}' AND expire_at > '{datetime.now().isoformat()}'")
    token_entry = cur.fetchone()
    if token_entry:
        return jsonify({'message': 'Токен действителен'}), 200
    else:
        return jsonify({'message': 'Токен не действителен'}), 401
    
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
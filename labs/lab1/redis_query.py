import redis

def get_student_data(code:str)->str:
    r = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )
    return r.get(code)
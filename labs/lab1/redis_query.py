import redis

def get_student_data(id:str)->str:
    r = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )
    return r.hget(key=id, name="fullname"), r.hget(key=id, name="code")
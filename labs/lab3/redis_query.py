import redis

def get_student_data(id:str)->str:
    r = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )
    result = r.hmget(id, "fullname", "code")
    return result[0], result[1]
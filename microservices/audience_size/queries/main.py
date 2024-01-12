from queries.neo4j_query import get_class_volumes

def get_audience_size(course:str, start_date:str, end_date:str) -> list:
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
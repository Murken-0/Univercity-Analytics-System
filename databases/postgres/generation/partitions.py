# Импортируем модуль для работы с датами
from datetime import datetime, timedelta

# Год для которого нужно создать партиции
year = 2022

# Открываем файл для записи инструкций
filename = "partition_instructions.sql"
with open(filename, "w") as file:
    # Генерируем инструкции для каждой недели
    for week_num in range(1, 53):
        # Получаем начальную и конечную даты для текущей недели
        start_date = datetime.strptime(f"{year}-W{week_num:02d}-0", "%Y-W%U-%w") + timedelta(days=1)
        end_date = start_date + timedelta(days=7)

        # Формируем инструкцию для текущей недели
        instruction = f"CREATE TABLE attendances_y{year}_w{week_num} PARTITION OF attendances\n"
        instruction += f"    FOR VALUES FROM ('{start_date.strftime('%Y-%m-%d')}') TO ('{end_date.strftime('%Y-%m-%d')}');\n"

        # Записываем инструкцию в файл
        file.write(instruction)

# Выводим сообщение об успешном завершении
print(f"Файл {filename} успешно создан.")
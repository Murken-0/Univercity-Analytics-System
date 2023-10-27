--1 +
INSERT INTO universities(title, inn)
VALUES ('МИРЭА', 123);

--2 +
INSERT INTO institutes(title, university_id)
VALUES ('ИКБ', 3);

--6 +
INSERT INTO departments(code, title, institute_id)
VALUES ('КБ-3','Рарзработка безопасных решений', 1);

--6 +
INSERT INTO specialities(code, title, department_id)
VALUES ('09.03.02','Долбаебы', 1);

--20 +
INSERT INTO groups(title, speciality_id)
VALUES ('БСБО-01-20', 1);

--500 +
INSERT INTO students(fio,code, group_id)
VALUES ('Иванов Иван Иванович', '20M200',1);

--50
INSERT INTO courses(title, description, scheduled_hours, special_department, department_id)
VALUES ('Разработка чего то умного','Ебашьте и все получится',120,TRUE,1);


INSERT INTO classes(type,date, description, equipment, course_id)
VALUES ('lection', '2023-10-22', 'Делали что то умное', 'Подушка для жопы', 1);

INSERT INTO student_course(course_id, student_id)
VALUES ();

CALL insert_attendances(1, 1);

CALL insert_attendances(1, 1, True);

SELECT group_id, COUNT(*) FROM students, groups WHERE students.group_id = groups.id GROUP BY group_id ORDER BY group_id

SELECT classes.id FROM classes 
JOIN courses ON classes.course_id = courses.id
JOIN student_course ON student_course.course_id = courses.id
JOIN students ON student_course.student_id = students.id
WHERE students.id = 501;

SELECT id FROM students WHERE group_id IN (1, 2, 5);
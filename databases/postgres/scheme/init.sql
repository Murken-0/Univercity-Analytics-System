--tables
CREATE TABLE schedule(
    id SERIAL PRIMARY KEY,
    class_id BIGINT NOT NULL,
    group_id BIGINT NOT NULL,
    date DATE NOT NULL,
    pair_number INTEGER NOT NULL
);

CREATE TABLE departments(
    id SERIAL PRIMARY KEY,
    code TEXT NOT NULL,
    title TEXT NOT NULL,
    institute_id BIGINT NOT NULL
);

CREATE TABLE courses(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    scheduled_hours INTEGER NOT NULL,
    department_id BIGINT NOT NULL
);

CREATE TABLE institutes(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    university_id BIGINT NOT NULL
);

CREATE TABLE attendances(
    id SERIAL,
    schedule_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    attended BOOLEAN NOT NULL,
    schedule_date DATE NOT NULL,
    CONSTRAINT attendances_pkey PRIMARY KEY (id, schedule_date)
) PARTITION BY RANGE (schedule_date);

CREATE TABLE students(
    id SERIAL PRIMARY KEY,
    fullname TEXT NOT NULL,
    code VARCHAR(6) UNIQUE NOT NULL,
    group_id BIGINT NOT NULL
);

CREATE TABLE specialities(
    id SERIAL PRIMARY KEY,
    code TEXT NOT NULL,
    title TEXT NOT NULL
);

CREATE TABLE group_course(
    id SERIAL PRIMARY KEY,
    group_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL,
    special BOOLEAN NOT NULL
);

CREATE TABLE class_type(
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL
);

CREATE TABLE department_speciality(
    id SERIAL PRIMARY KEY,
    department_id BIGINT NOT NULL,
    speciality_id BIGINT NOT NULL
);

CREATE TABLE groups(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    speciality_id BIGINT NOT NULL,
    department_id BIGINT NOT NULL
);

CREATE TABLE classes(
    id SERIAL PRIMARY KEY,
    type_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    equipment TEXT NOT NULL,
    course_id BIGINT NOT NULL
);

CREATE TABLE class_materials(
    id SERIAL PRIMARY KEY,
    class_id BIGINT NOT NULL,
    file TEXT NOT NULL
);

CREATE TABLE universities(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL
);

ALTER TABLE
    department_speciality ADD CONSTRAINT department_speciality_speciality_id_foreign FOREIGN KEY(speciality_id) REFERENCES specialities(id);
ALTER TABLE
    group_course ADD CONSTRAINT group_course_course_id_foreign FOREIGN KEY(course_id) REFERENCES courses(id);
ALTER TABLE
    groups ADD CONSTRAINT groups_department_id_foreign FOREIGN KEY(department_id) REFERENCES departments(id);
ALTER TABLE
    attendances ADD CONSTRAINT attendances_student_id_foreign FOREIGN KEY(student_id) REFERENCES students(id);
ALTER TABLE
    attendances ADD CONSTRAINT attendances_schedule_id_foreign FOREIGN KEY(schedule_id) REFERENCES schedule(id);
ALTER TABLE
    departments ADD CONSTRAINT departments_institute_id_foreign FOREIGN KEY(institute_id) REFERENCES institutes(id);
ALTER TABLE
    department_speciality ADD CONSTRAINT department_speciality_department_id_foreign FOREIGN KEY(department_id) REFERENCES departments(id);
ALTER TABLE
    groups ADD CONSTRAINT groups_speciality_id_foreign FOREIGN KEY(speciality_id) REFERENCES specialities(id);
ALTER TABLE
    group_course ADD CONSTRAINT group_course_group_id_foreign FOREIGN KEY(group_id) REFERENCES groups(id);
ALTER TABLE
    classes ADD CONSTRAINT classes_type_id_foreign FOREIGN KEY(type_id) REFERENCES class_type(id);
ALTER TABLE
    students ADD CONSTRAINT students_group_id_foreign FOREIGN KEY(group_id) REFERENCES groups(id);
ALTER TABLE
    schedule ADD CONSTRAINT schedule_class_id_foreign FOREIGN KEY(class_id) REFERENCES classes(id);
ALTER TABLE
    courses ADD CONSTRAINT courses_department_id_foreign FOREIGN KEY(department_id) REFERENCES departments(id);
ALTER TABLE
    classes ADD CONSTRAINT classes_course_id_foreign FOREIGN KEY(course_id) REFERENCES courses(id);
ALTER TABLE
    class_materials ADD CONSTRAINT class_materials_class_id_foreign FOREIGN KEY(class_id) REFERENCES classes(id);
ALTER TABLE
    institutes ADD CONSTRAINT institutes_university_id_foreign FOREIGN KEY(university_id) REFERENCES universities(id);
ALTER TABLE
    schedule ADD CONSTRAINT schedule_group_id_foreign FOREIGN KEY(group_id) REFERENCES groups(id);

CREATE OR REPLACE PROCEDURE insert_attendances(student_i BIGINT, schedule_i BIGINT, attended BOOLEAN) LANGUAGE plpgsql 
AS $$
DECLARE
    _date TIMESTAMP WITHOUT TIME ZONE;
BEGIN
_date := (SELECT date FROM schedule WHERE id = schedule_i);
INSERT INTO attendances(student_id, schedule_id, attended, schedule_date)
    VALUES (student_i, schedule_i, attended, _date);
END
$$;

/*
CREATE TABLE IF NOT EXISTS lections
(
    id INT GENERATED ALWAYS AS IDENTITY,
    date_time DATE NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS students
(
    id INT GENERATED ALWAYS AS IDENTITY,
    code VARCHAR(7) NOT NULL,
    group_code VARCHAR(12) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS visits
(
    id INT GENERATED ALWAYS AS IDENTITY,
    lection_id int,
    student_id int,
    lection_date timestamp,
    PRIMARY KEY(id),
    CONSTRAINT fk_lection
      FOREIGN KEY(lection_id) 
    REFERENCES lections(id)
      ON DELETE CASCADE,
    CONSTRAINT fk_student
      FOREIGN KEY(student_id) 
    REFERENCES students(id)
      ON DELETE CASCADE
);

--date
CREATE OR REPLACE FUNCTION trg_attendances_date() RETURNS trigger AS $att_date$
    BEGIN
        NEW.class_date := (SELECT date FROM classes WHERE id = NEW.class_id);
        RETURN NEW;
    END;
$att_date$ LANGUAGE plpgsql;

--partitions
CREATE OR REPLACE FUNCTION trg_attendances() RETURNS trigger AS $func$
DECLARE
    _tbl text;
    _rec_date date;
    _min_date date;
    _max_date date;
BEGIN
NEW.class_date := (SELECT date FROM classes WHERE id = NEW.class_id);
_tbl := to_char(NEW.class_date, 'visits_yIYYY_wIW');
_rec_date := NEW.class_date::date;
_min_date := date_trunc('week', NEW.class_date)::date;
_max_date := date_trunc('week', NEW.class_date)::date + 7;

IF NOT EXISTS (
    SELECT 1
    FROM   pg_catalog.pg_class c
    JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace
    WHERE  n.nspname = 'public'
    AND    c.relname = _tbl
    AND    c.relkind = 'r') THEN
    EXECUTE format('CREATE TABLE IF NOT EXISTS %I PARTITION OF attendances
                        FOR VALUES FROM (''%L'') TO (''%L'');'
            , _tbl
            , to_char(_min_date, 'YYYY-MM-DD')
            , to_char(_max_date, 'YYYY-MM-DD'));
END IF;
RETURN NEW;
END
$func$ LANGUAGE plpgsql;
*/
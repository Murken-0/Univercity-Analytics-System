--tables
CREATE TABLE departments(
    id SERIAL PRIMARY KEY,
    code TEXT NOT NULL,
    title TEXT NOT NULL,
    institute_id BIGINT NOT NULL
);

CREATE TABLE courses(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    scheduled_hours INTEGER NOT NULL,
    special_department BOOLEAN NOT NULL,
    department_id BIGINT NOT NULL
);

CREATE TABLE institutes(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    university_id BIGINT NOT NULL
);

CREATE TABLE attendances(
    id SERIAL,
    class_id BIGINT NOT NULL,
    student_id BIGINT NOT NULL,
    attended BOOLEAN NOT NULL,
    class_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    CONSTRAINT attendances_pkey PRIMARY KEY (id, class_date)
) PARTITION BY RANGE (class_date);

CREATE TABLE students(
    id SERIAL PRIMARY KEY,
    fio TEXT NOT NULL,
    code VARCHAR(6) NOT NULL UNIQUE,
    group_id BIGINT NOT NULL
);

CREATE TABLE specialities(
    id SERIAL PRIMARY KEY,
    code TEXT NOT NULL,
    title TEXT NOT NULL,
    department_id BIGINT NOT NULL
);

CREATE TABLE student_course(
    id SERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL,
    course_id BIGINT NOT NULL
);

CREATE TABLE groups(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    speciality_id BIGINT NOT NULL
);

CREATE TABLE classes(
    id SERIAL PRIMARY KEY,
    type VARCHAR(255) CHECK (type IN('lection', 'practice')) NOT NULL,
    date TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    description TEXT NOT NULL,
    equipment TEXT NOT NULL,
    course_id BIGINT NOT NULL
);

CREATE TABLE universities(
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    inn BIGINT NOT NULL
);

--foreign keys
ALTER TABLE
    student_course ADD CONSTRAINT student_course_course_id_foreign FOREIGN KEY(course_id) REFERENCES courses(id);
ALTER TABLE
    student_course ADD CONSTRAINT student_course_student_id_foreign FOREIGN KEY(student_id) REFERENCES students(id);
ALTER TABLE
    attendances ADD CONSTRAINT attendances_student_id_foreign FOREIGN KEY(student_id) REFERENCES students(id);
ALTER TABLE
    attendances ADD CONSTRAINT attendances_class_id_foreign FOREIGN KEY(class_id) REFERENCES classes(id);
ALTER TABLE
    groups ADD CONSTRAINT groups_speciality_id_foreign FOREIGN KEY(speciality_id) REFERENCES specialities(id);
ALTER TABLE
    students ADD CONSTRAINT students_group_id_foreign FOREIGN KEY(group_id) REFERENCES groups(id);
ALTER TABLE
    courses ADD CONSTRAINT courses_department_id_foreign FOREIGN KEY(department_id) REFERENCES departments(id);
ALTER TABLE
    classes ADD CONSTRAINT classes_course_id_foreign FOREIGN KEY(course_id) REFERENCES courses(id);
ALTER TABLE
    specialities ADD CONSTRAINT specialities_department_id_foreign FOREIGN KEY(department_id) REFERENCES departments(id);
ALTER TABLE
    institutes ADD CONSTRAINT institutes_university_id_foreign FOREIGN KEY(university_id) REFERENCES universities(id);
ALTER TABLE
    departments ADD CONSTRAINT departments_institute_id_foreign FOREIGN KEY(institute_id) REFERENCES institutes(id);

CREATE OR REPLACE PROCEDURE insert_attendances(student_i BIGINT, class_i BIGINT, attended BOOLEAN) LANGUAGE plpgsql 
AS $$
DECLARE
    _date TIMESTAMP WITHOUT TIME ZONE;
BEGIN
_date := (SELECT date FROM classes WHERE id = class_i);
INSERT INTO attendances(student_id, class_id, attended, class_date)
    VALUES (student_i, class_i, attended, _date);
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
_tbl := to_char(NEW.class_date, '"visits_y"IYYY_"w"IW');
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
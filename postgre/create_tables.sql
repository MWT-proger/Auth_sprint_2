
-- Создание отдельной схемы для контента:
CREATE SCHEMA content;

--  Информация о фильмах:
CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    certificate TEXT,
    file_path TEXT,
    rating FLOAT,
    type TEXT not null,
    created timestamp with time zone,
    modified timestamp with time zone
);

-- Жанры кинопроизведений:
CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

-- Создание таблицы связи жанров с кинопроизведениями:
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    created timestamp with time zone,
    UNIQUE (film_work_id, genre_id)
);

-- Участники фильмов:
CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_date DATE,
    created timestamp with time zone,
    modified timestamp with time zone
);

-- Создание таблицы связи участников с кинопроизведениями:
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role TEXT not null,
    created timestamp with time zone,
    modified timestamp with time zone,
    UNIQUE (film_work_id, person_id, role)
);
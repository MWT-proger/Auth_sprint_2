-- Создание схемы для контента;
CREATE SCHEMA IF NOT EXISTS content;

-- Создание таблицы  ролей:
CREATE TABLE IF NOT EXISTS content.roles (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

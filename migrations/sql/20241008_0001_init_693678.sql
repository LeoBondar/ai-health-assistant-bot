CREATE SCHEMA IF NOT EXISTS rnd;

CREATE TABLE IF NOT EXISTS rnd.logs(
    id            UUID                                PRIMARY KEY,
    chat_id       BIGINT                              NOT NULL,
    user_id       BIGINT                              NOT NULL,
    type          VARCHAR(255)                        NOT NULL,
    request       VARCHAR(255)                        NOT NULL,
    response      VARCHAR(255)                        NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
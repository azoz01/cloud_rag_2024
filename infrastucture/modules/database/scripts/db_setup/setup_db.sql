CREATE SEQUENCE table_name_id_seq;

CREATE TABLE user_history (
    id INTEGER NOT NULL DEFAULT nextval('table_name_id_seq') PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    prompt VARCHAR(1000) NOT NULL,
    response VARCHAR(1000) NOT NULL
);
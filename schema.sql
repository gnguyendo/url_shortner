DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    original_url TEXT NOT NULL PRIMARY KEY,
    shortened_url TEXT NOT NULL
);

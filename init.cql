-- Create a keyspace
CREATE KEYSPACE IF NOT EXISTS url_shortener WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };

-- Create a table
CREATE TABLE IF NOT EXISTS url_shortener.urls (
key text PRIMARY KEY,
reference text,
owner_id int,
action text,
is_active boolean
);
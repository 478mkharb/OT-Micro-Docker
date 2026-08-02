CREATE KEYSPACE IF NOT EXISTS employee_db
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE employee_db;
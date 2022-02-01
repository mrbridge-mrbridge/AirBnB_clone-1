-- prepare a MySQL server
CREATE DATABASE hbnb_dev_db IF NOT EXISTS
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd'
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost'
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost'

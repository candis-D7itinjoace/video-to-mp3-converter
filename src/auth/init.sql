    CREATE USER 'auth'@'localhost' IDENTIFIED BY '1234';
    CREATE database auth_db;
    GRANT ALL PRIVILEGES ON auth_db.* TO 'auth'@'localhost';

    USE auth_db;


    CREATE TABLE user (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );


    INSERT INTO user (email, password) VALUES ('bjaoui.bayrem@gmail.com', 'sp33ztr');
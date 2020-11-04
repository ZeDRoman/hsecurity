DROP TABLE IF EXISTS users, pass;

CREATE TABLE users(
  id INT NOT NULL,
  login VARCHAR (20) NOT NULL,
  money_amount  INT NOT NULL,
  card_number  VARCHAR (20),
  status TINYINT,
  PRIMARY KEY (id)
);

INSERT INTO users VALUES(0,'admin',500, '1234567891234567', 1);
INSERT INTO users VALUES(1,'user1',500, '1234567891234561', 1);
INSERT INTO users VALUES(2,'user2',100, '1234567891234562', 0);
INSERT INTO users VALUES(3,'user3',0, '1234567891234563', 1);
INSERT INTO users VALUES(4,'user4',5000000, '1234567891234564', 0);

CREATE TABLE pass(
  id INT NOT NULL,
  password VARCHAR(100),
  PRIMARY KEY (id)
);

INSERT INTO pass VALUES(0, 'helloworld');
INSERT INTO pass VALUES(1, '1');
INSERT INTO pass VALUES(2, '2');
INSERT INTO pass VALUES(3, '3');
INSERT INTO pass VALUES(4, '4');

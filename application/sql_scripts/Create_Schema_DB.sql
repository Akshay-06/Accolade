-- Database: Accolade

-- DROP DATABASE IF EXISTS "Accolade";

CREATE DATABASE "Accolade"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


Create table login_details (
id serial PRIMARY KEY,
Emp_id serial not null,
Emp_Email VARCHAR(100) NOT NULL,
Emp_pass VARCHAR(100) not null,
Created_At timestamp not null,
Created_By Varchar(100),
Modified_At Timestamp,
modified_by varchar(100),
FOREIGN KEY (Emp_id)
      REFERENCES employee (emp_id)
);


Create table employee (
Emp_id serial primary key not null,
Emp_Name VARCHAR(100) NOT NULL,
Emp_Email VARCHAR(100) not null,
Created_At timestamp not null,
Created_By Varchar(100),
Modified_At Timestamp,
modified_by varchar(100)
);

Create table Dashboard_data (
user_id varchar(500) PRIMARY KEY,
reputation int NOT NULL,
total_answers int not null,
answers_accepted int,
total_score int,
Created_At timestamp not null,
Created_By Varchar(100),
Modified_At Timestamp,
modified_by varchar(100),
answers_rejected int,
reward_points int
);
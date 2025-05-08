-- DROP TABLES
DROP TABLE IF EXISTS salon_service CASCADE;
DROP TABLE IF EXISTS salon_report CASCADE;
DROP TABLE IF EXISTS salon_appointment CASCADE;
DROP TABLE IF EXISTS salon_user CASCADE;

-- SALON_USER TABLE
CREATE TABLE salon_user (
    user_id SERIAL PRIMARY KEY,
    active BOOLEAN DEFAULT TRUE,
    user_type VARCHAR(15) DEFAULT 'client',
    access_level SMALLINT DEFAULT 1,
    user_name VARCHAR(15) NOT NULL,
    email VARCHAR(120) NOT NULL,
    user_image VARCHAR(30) DEFAULT 'default-user.png',
    password VARCHAR(80) NOT NULL,
    phone_number VARCHAR(15) DEFAULT 'CSIT',
    address VARCHAR(15) DEFAULT 'CS',
    age SMALLINT DEFAULT 18,
    pay_rate DECIMAL(5,2) DEFAULT 15.75,
    speciality VARCHAR(15) DEFAULT 'Hair-dresser',
    CONSTRAINT unique_salon_client UNIQUE (user_name, email)
);

 
-- $2b$12$gqsQ8F1vZRxuRj.k2PM57eL/NA.Y/b6FxJ0SfihztJdlcPw7q2E9G'
-- >>> gen_pw('12')
-- '$2b$12$X6WVyVmfu98fH7KxjDYSCuPCqAnJa/o.RHaPxZi6Ojgq0u4ZXo6Vm'
-- >>> gen_pw('13')
-- '$2b$12$q69QDA9zTxE3z1alMe4Nzuk2i6h4RP6TFkhriRm1vjwurnMApdg9i'

--------------  admins -----------------
INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
      VALUES ('admin',2,'nasr','nasrs@email.com',  '$2b$12$gqsQ8F1vZRxuRj.k2PM57eL/NA.Y/b6FxJ0SfihztJdlcPw7q2E9G', '514-1234567', 'addr1', 50 ); 

INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
      VALUES ('admin',2,'badr','badr@email.com',  '$2b$12$gqsQ8F1vZRxuRj.k2PM57eL/NA.Y/b6FxJ0SfihztJdlcPw7q2E9G', '514-1234567', 'addr2', 18 ); 
----------- Clients (customers) ---------------------------[3 6]  
INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
      VALUES ('client',1,'client1','client1@email.com',  '$2b$12$X6WVyVmfu98fH7KxjDYSCuPCqAnJa/o.RHaPxZi6Ojgq0u4ZXo6Vm', '514-1234567', 'laval',22 ); 
INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
  VALUES ('client',1,'client2','client2@email.com',  '$2b$12$X6WVyVmfu98fH7KxjDYSCuPCqAnJa/o.RHaPxZi6Ojgq0u4ZXo6Vm', '514-1234567', 'laval',23 ); 
  INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
      VALUES ('client',1,'client3','client3@email.com',  '$2b$12$X6WVyVmfu98fH7KxjDYSCuPCqAnJa/o.RHaPxZi6Ojgq0u4ZXo6Vm', '514-1234567', 'laval',22 ); 
INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
  VALUES ('client',1,'client4','client4@email.com',  '$2b$12$X6WVyVmfu98fH7KxjDYSCuPCqemployeeAnJa/o.RHaPxZi6Ojgq0u4ZXo6Vm', '514-1234567', 'laval',23 ); 
----------- 0 Students ---------------------------  [7]
INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
  VALUES ( 'client',1,'client10eng','client10eng@email.com',  '$2b$12$X6WVyVmfu98fH7KxjDYSCuPCqAnJa/o.RHaPxZi6Ojgq0u4ZXo6Vm', '514-4567890', 'Montreal', 24  ); 
----------- Phy Students ---------------------------  [8]
INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
  VALUES ( 'client',1,'client1phy','client1phy@email.com',  '$2b$12$X6WVyVmfu98fH7KxjDYSCuPCqAnJa/o.RHaPxZi6Ojgq0u4ZXo6Vm', 'phy', 'Sce', 2022 ); 
----------  Teachers ------------------------------- [9 11, 12 13, 14 15]
INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
  VALUES ('professional',1,'employee1','employee1@email.com',  '$2b$12$X6WVyVmfu98fH7KxjDYSCuPCqAnJa/o.RHaPxZi6Ojgq0u4ZXo6Vm', '514-1234567', 'laval',22 ); 
INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
  VALUES ('professional',1,'employee2','employee1@email.com',  '$2b$12$X6WVyVmfu98fH7KxjDYSCuPCqAnJa/o.RHaPxZi6Ojgq0u4ZXo6Vm', '514-1234567', 'laval',22 ); 
INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
  VALUES ('professional',1,'employee3','employee1@email.com',  '$2b$12$X6WVyVmfu98fH7KxjDYSCuPCqAnJa/o.RHaPxZi6Ojgq0u4ZXo6Vm', '514-1234567', 'laval',22 ); 
--------------------------------------------
INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
  VALUES ('professional',1,'employee4','employee1@email.com',  '$2b$12$X6WVyVmfu98fH7KxjDYSCuPCqAnJa/o.RHaPxZi6Ojgq0u4ZXo6Vm', '514-4567890', 'Montreal', 24  ); 
INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
  VALUES ('professional',1,'employee5','employee1@email.com',  '$2b$12$X6WVyVmfu98fH7KxjDYSCuPCqAnJa/o.RHaPxZi6Ojgq0u4ZXo6Vm', '514-4567890', 'Montreal', 24  ); 
--------------------------------------------
INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
  VALUES ('professional',1,'employee6','employee1@email.com',  '$2b$12$X6WVyVmfu98fH7KxjDYSCuPCqAnJa/o.RHaPxZi6Ojgq0u4ZXo6Vm', '438-12345678', 'ottawa', 28 ); 
INSERT INTO SALON_USER ( user_type ,access_level , user_name   ,email ,  password, phone_number, address, age )
  VALUES ('professional',1,'employee7','employee1@email.com',  '$2b$12$X6WVyVmfu98fH7KxjDYSCuPCqAnJa/o.RHaPxZi6Ojgq0u4ZXo6Vm', '438-12345678', 'ottawa', 28 );
 
-- -------------------------------------------------

-- SALON_APPOINTMENT TABLE
CREATE TABLE salon_appointment (
    appointment_id SERIAL PRIMARY KEY,
    status VARCHAR(10) DEFAULT 'requested',
    approved BOOLEAN DEFAULT FALSE,
    date_appoint DATE DEFAULT CURRENT_DATE,
    slot VARCHAR(10) DEFAULT '9-10',
    venue VARCHAR(20) DEFAULT 'cmn_room',
    
    consumer_id INTEGER NOT NULL,
    provider_id INTEGER NOT NULL,
    consumer_name VARCHAR(15) NOT NULL,
    provider_name VARCHAR(15) NOT NULL,
    nber_services SMALLINT DEFAULT 1,
    
    consumer_report VARCHAR(500),

    FOREIGN KEY (consumer_id) REFERENCES salon_user(user_id),
    FOREIGN KEY (provider_id) REFERENCES salon_user(user_id)
);


   
INSERT INTO SALON_APPOINTMENT (appointment_id, status ,slot ,venue ,consumer_id  ,provider_id,  consumer_name, provider_name)  VALUES 
            (1, 'requested', '10-11', 'room1', 3, 9, 'client1', 'employee1');
INSERT INTO SALON_APPOINTMENT (appointment_id, status ,slot ,venue ,consumer_id  ,provider_id,  consumer_name, provider_name)  VALUES 
 (2, 'requested', '9-10', 'room2', 3, 11, 'client1', 'employee3');
INSERT INTO SALON_APPOINTMENT (appointment_id, status ,slot ,venue ,consumer_id  ,provider_id,  consumer_name, provider_name) VALUES  
(3, 'requested', '3-4', 'chair1', 4,10, 'client2', 'employee2');
INSERT INTO SALON_APPOINTMENT (appointment_id, status ,slot ,venue ,consumer_id  ,provider_id,  consumer_name, provider_name) VALUES  
  (4, 'requested', '3-4', 'chair2', 7,12, 'client3', 'employee3' );

 
-- -------------------------------------------------
--------------------------
-- SALON_REPORT TABLE
CREATE TABLE salon_report (
    report_id SERIAL PRIMARY KEY,
    appointment_id INTEGER,
    status VARCHAR(10) DEFAULT 'inactive',
    date_report DATE DEFAULT CURRENT_DATE,
    feedback_professional VARCHAR(500),
    feedback_client VARCHAR(500),
    FOREIGN KEY (appointment_id) REFERENCES salon_appointment(appointment_id)
);

   
INSERT INTO SALON_REPORT (appointment_id, status ,feedback_client ,feedback_professional) VALUES  
  (1, 'closed', 'was a good hour', 'any time' );
INSERT INTO SALON_REPORT (appointment_id, status ,feedback_client ,feedback_professional) VALUES  
  (2, 'grieve', 'Discrimination', 'any thing from this entitled client!' );
INSERT INTO SALON_REPORT (appointment_id, status ,feedback_client ,feedback_professional) VALUES 
 (3, 'closed', 'nice job', 'thansk!' );
INSERT INTO SALON_REPORT (appointment_id, status ,feedback_client ,feedback_professional) VALUES 
   (4, 'done', 'ok', 'ok??' );
COMMIT;
--------------SALON_SERVICE___________________
--CREATE TABLE SALON_SERVICE
--(service_id NUMBER(4) GENERATED BY DEFAULT AS IDENTITY,
--appointment_id  NUMBER(4) ,
--service_name  VARCHAR(35) default ('inactive'),  --closed, done, grieve, complaint,
--service_duration  Number(1) default (1),  --closed, done, grieve, complaint,
--service_price  Decimal(5,2) ,
--service_materials  VARCHAR(35) default ('inactive'),  --closed, done, grieve, complaint,
--CONSTRAINT  salon_service_pk PRIMARY KEY(service_id),
--CONSTRAINT salon_servicet_fk FOREIGN KEY (appointment_id) REFERENCES SALON_APPOINTMENT (appointment_id)
--); 

   
--INSERT INTO SALON_SERVICE (appointment_id, status ,feedback_client ,feedback_professional) VALUES  (1, 'closed', 'was a good hour', 'any time' );
--INSERT INTO SALON_SERVICE (appointment_id, status ,feedback_client ,feedback_professional) VALUES  (2, 'grieve', 'Discrimination', 'any thing from this entitled clientent!' );
--INSERT INTO SALON_SERVICE (appointment_id, status ,feedback_client ,feedback_professional) VALUES  (3, 'closed', 'ok', 'only ok!' );
--INSERT INTO SALON_SERVICE (appointment_id, status ,feedback_client ,feedback_professional) VALUES  (4, 'done', NULL, NULL );

-- SELECT * FROM SALON_USER;
-- SELECT * FROM SALON_APPOINTMENT;
-- --
-- select COLUMN_NAME from ALL_TAB_COLUMNS where TABLE_NAME='SALON_USER';
-- select COLUMN_NAME from ALL_TAB_COLUMNS where TABLE_NAME='SALON_APPOINTMENT';
-- select COLUMN_NAME from ALL_TAB_COLUMNS where TABLE_NAME='SALON_REPORT';
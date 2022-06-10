use HDTherapist;

-- FUNCTION TO CHECK HOW MANY TUPLES OF THE SAME REGISTRATION USERNAME EXIST WITHIN THE DATABSE

DROP FUNCTION IF EXISTS duplicate_check;

DELIMITER $$

CREATE FUNCTION duplicate_check(dc_id VARCHAR(15))
RETURNS INT
DETERMINISTIC
BEGIN
DECLARE dc_frequency INT;
SELECT COUNT(*) INTO dc_frequency
FROM REGISTRATION 
WHERE username = dc_id;
RETURN dc_frequency;
END $$

DELIMITER ;

-- SELECT duplicate_check('abc');

-- PRODECDURE TO REGISTER A USER
DROP PROCEDURE IF EXISTS register_user;

DELIMITER $$

CREATE PROCEDURE register_user(IN r_user VARCHAR(15), IN r_pw VARCHAR(15),
    IN r_name VARCHAR(20), IN r_is_patient bool, IN r_gender enum("male","female"),
    IN r_race VARCHAR(50), IN r_age INT)
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Register failed';
INSERT INTO REGISTRATION (username, pw, p_name, is_patient, gender, race, age) values (r_user, r_pw, r_name, r_is_patient, r_gender, r_race, r_age);
END $$	

DELIMITER ;

-- SELECT duplicate_check('abc');
-- CALL register_user('abc', 'abc', 'abc', FALSE, 'male', 'abc', 10);

-- FUNCTION TO CHECK IF THE PASSWORD IS CORRECT FOR THE GIVEN USER

DROP FUNCTION IF EXISTS password_check;

DELIMITER $$

CREATE FUNCTION password_check(pwc_id VARCHAR(15), pwc_password VARCHAR(15))
RETURNS INT
DETERMINISTIC
BEGIN
DECLARE pwc_frequency INT;
SELECT COUNT(*) INTO pwc_frequency
FROM REGISTRATION 
WHERE username = pwc_id AND pw = pwc_password;
RETURN pwc_frequency;
END $$

DELIMITER ;

-- FUNCTION TO CHECK HOW MANY TUPLES OF THE SAME THERAPIST ID EXIST WITHIN THE DATABSE

DROP FUNCTION IF EXISTS num_therapist_check;

DELIMITER $$

CREATE FUNCTION num_therapist_check(ntc_tid VARCHAR(15))
RETURNS INT
DETERMINISTIC
BEGIN
DECLARE ntc_frequency INT;
SELECT COUNT(*) INTO ntc_frequency
FROM THERAPIST 
WHERE tid = ntc_tid;
RETURN ntc_frequency;
END $$

DELIMITER ;

-- PROCEDURE TO CREATE THERAPIST
DROP PROCEDURE IF EXISTS insert_therapist;

DELIMITER $$

CREATE PROCEDURE insert_therapist(IN it_tid VARCHAR(15), IN it_numPatients INT)
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Insert Therapist failed';
INSERT INTO THERAPIST (tid, numPatients) values (it_tid, it_numPatients);
END $$

DELIMITER ;

-- DELETE THERAPIST

DROP PROCEDURE IF EXISTS delete_therapist;

DELIMITER $$

CREATE PROCEDURE delete_therapist(IN dt_username VARCHAR(15))
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Delete Therapist failed';
DELETE FROM REGISTRATION 
WHERE username = dt_username;

END $$

DELIMITER ;

-- PROCEDURE TO UPDATE NUMBER OF PATIENTS FOR A THERAPIST
DROP PROCEDURE IF EXISTS update_num_patients;

DELIMITER $$

CREATE PROCEDURE update_num_patients(IN unp_tid VARCHAR(15), IN unp_amount INT)
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Update Number of Patients failed';
UPDATE THERAPIST 
SET numPatients = unp_amount WHERE tid = unp_tid;
END $$

DELIMITER ;

-- FUNCTION TO CHECK HOW MANY TUPLES OF THE SAME PATEINT ID EXIST WITHIN THE DATABSE

DROP FUNCTION IF EXISTS num_patient_check;

DELIMITER $$

CREATE FUNCTION num_patient_check(npc_personalID VARCHAR(15))
RETURNS INT
DETERMINISTIC
BEGIN
DECLARE npc_frequency INT;
SELECT COUNT(*) INTO npc_frequency
FROM PATIENT 
WHERE npc = npc_personalID;
RETURN npc_frequency;
END $$

DELIMITER ;

-- PROCEDURE TO CREATE PATIENT
DROP PROCEDURE IF EXISTS insert_patient;

DELIMITER $$

CREATE PROCEDURE insert_patient(IN ip_personalID VARCHAR(15), IN ip_notes VARCHAR(400))
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Insert Patient failed';
INSERT INTO PATIENT (personalID, notes) values (ip_personalID, ip_notes);
END $$

DELIMITER ;

-- CALL insert_patient('abc', 'abc');

-- PROCEDURE TO UPDATE NOTES OF A PATIENT
DROP PROCEDURE IF EXISTS update_note;

DELIMITER $$

CREATE PROCEDURE update_note(IN un_personalID VARCHAR(15), IN un_notes VARCHAR(400))
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Update Patient failed';
UPDATE PATIENT 
SET notes = un_notes WHERE personalID = un_personalID;
END $$

DELIMITER ;

-- RETURNS IF THE USER IS A PATIENT

DROP FUNCTION IF EXISTS isPatient_check;

DELIMITER $$

CREATE FUNCTION isPatient_check(ipc_id VARCHAR(15))
RETURNS BOOL
DETERMINISTIC
BEGIN
DECLARE ipc_is_patient BOOL;
SELECT is_patient INTO ipc_is_patient
FROM REGISTRATION 
WHERE username = ipc_id;
RETURN ipc_is_patient;
END $$

DELIMITER ;

-- INSERT GAME

DROP PROCEDURE IF EXISTS insert_game;

DELIMITER $$

CREATE PROCEDURE insert_game(IN ig_gid INT, IN ig_patientPlayed VARCHAR(15), IN ig_color VARCHAR(15), IN ig_score INT, IN ig_round INT, IN ig_time_limit INT)
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Insert Game failed';
INSERT INTO GAME (gid, patientPlayed, color, score, round, time_limit) values (ig_gid, ig_patientPlayed, ig_score, ig_color, ig_round, ig_time_limit);
END $$

DELIMITER ;

-- INSERT QUESTION

DROP PROCEDURE IF EXISTS insert_question;

DELIMITER $$

CREATE PROCEDURE insert_question(IN iq_qid INT, IN iq_questionText VARCHAR(100), IN questionOrder INT)
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Insert Question failed';
INSERT INTO QUESTION (qid, questionText, questionOrder) values (iq_qid, iq_questionText, questionOrder);
END $$

DELIMITER ;

CALL insert_question (1, "Did anything happen today that made you upset?", 1);
CALL insert_question (2, "Did you read or see anything that got you thinking hard?", 2);
CALL insert_question (3, "Did you do anything that was challenging and how did it make you feel?", 3);
CALL insert_question (4, "Did you show kindness to anyone today?", 4);
CALL insert_question (5, "What is one thing you liked about your day?", 5);
CALL insert_question (6, "If you can change something about your day, what would it be?", 6);
CALL insert_question (7, "Did someone say anything that made you upset today?", 7);
CALL insert_question (8, "Did you ask for help from anyone today?", 8);
CALL insert_question (9, "What are you most grateful about today?", 9);
CALL insert_question (10, "What is the favourite part of your day?", 10);
CALL insert_question (11, "What are you most thankful for today?", 11);
CALL insert_question (12, "One the scale of 1 to 10 (1 being worst, 10 being best) how do you feel?", 12);

-- UPDATE QUESTION

DROP PROCEDURE IF EXISTS update_question;

DELIMITER $$

CREATE PROCEDURE update_question(IN uq_qid INT, IN uq_questionText VARCHAR(100), IN uq_questionOrder INT)
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Update Question failed';
UPDATE QUESTION 
SET questionText = uq_questionText AND questionOrder = uq_questionOrder WHERE qid = uq_qid;
END $$

DELIMITER ;

-- DELETE QUESTION

DROP PROCEDURE IF EXISTS delete_question;

DELIMITER $$

CREATE PROCEDURE delete_question(IN dq_qid INT)
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Delete Question failed';
DELETE FROM QUESTION 
WHERE qid = uq_qid;

END $$

DELIMITER ;

-- VIEW QUESTION TEXT

DROP FUNCTION IF EXISTS view_question_text;

DELIMITER $$

CREATE FUNCTION view_question_text(vqt_id INT)
RETURNS VARCHAR(100)
DETERMINISTIC
BEGIN
DECLARE vq_text VARCHAR(100);
SELECT questionText INTO vq_text
FROM QUESTION 
WHERE qid = vqt_id;
RETURN vq_text;
END $$

DELIMITER ;

-- INSERT ANSWER

DROP PROCEDURE IF EXISTS insert_answer;

DELIMITER $$

CREATE PROCEDURE insert_answer(IN ia_aid INT, IN ia_qid INT, IN ia_patientID VARCHAR(15), IN ia_response VARCHAR(1500))
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Insert Answer failed';
INSERT INTO ANSWER (aid, qid, patientID, response) values (ia_aid, ia_qid, ia_patientID, ia_response);
END $$

DELIMITER ;

-- UPDATE ANSWER

DROP PROCEDURE IF EXISTS update_answer;

DELIMITER $$

CREATE PROCEDURE update_answer(IN uq_aid INT, IN uq_qid INT, IN uq_patientID VARCHAR(20), IN uq_response VARCHAR(1500))
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Update Answer failed';
UPDATE ANSWER 
SET patientID = uq_patientID AND response = uq_response WHERE aid = ia_aid;
END $$

DELIMITER ;

-- DELETE ANSWER
DROP PROCEDURE IF EXISTS delete_answer;

DELIMITER $$

CREATE PROCEDURE delete_answer(IN da_aid INT)
BEGIN
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SELECT 'Delete Answer failed';
DELETE FROM ANSWER 
WHERE aid = da_aid;

END $$

DELIMITER ;





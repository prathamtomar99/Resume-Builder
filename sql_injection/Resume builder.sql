CREATE DATABASE resumeBuilderDB;
USE resumeBuilderDB;

# USER TABLE
CREATE TABLE `resumebuilderdb`.`user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `name` TEXT NOT NULL,
  `email` VARCHAR(100) NULL,
  `dept` VARCHAR(60) NOT NULL,
  `phone` BIGINT NULL,
  `prn` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `phone_UNIQUE` (`phone` ASC) VISIBLE,
  UNIQUE INDEX `prn_UNIQUE` (`prn` ASC) VISIBLE
);

# USER RECORD TABLE
CREATE TABLE `resumebuilderdb`.`user_record` (
  `Action` VARCHAR(10) NOT NULL,
  `old_user_id` INT NULL,
  `new_user_id` INT NULL,
  `log_time` TIME NOT NULL
);
  
# RESUME TABLE
CREATE TABLE resume (
	resume_id VARCHAR(6) PRIMARY KEY NOT NULL,
    user_id INT,
    languages_known TEXT,
    achievements TEXT,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

# SKILL TABLE
CREATE TABLE skills (
	skill_id INT PRIMARY KEY NOT NULL,
    resume_id VARCHAR(6),
    skill_name TEXT NOT NULL,
    proficiency_level VARCHAR(15) NOT NULL,
    certificate TEXT,
    FOREIGN KEY (resume_id) REFERENCES resume(resume_id)
);

# EDUCATION TABLE
CREATE TABLE education (
	edu_id INT PRIMARY KEY NOT NULL,
    resume_id VARCHAR(6),
    degree_name VARCHAR(60) NOT NULL,
    institution_name TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL ,
    grade_CGPA FLOAT NOT NULL,
    FOREIGN KEY (resume_id) REFERENCES resume(resume_id),
    CHECK(end_date > start_date)
);

# EXPERIENCE TABLE
CREATE TABLE resumebuilderdb.experience (
  experience_id INT NOT NULL,
  resume_id VARCHAR(6),
  job_title VARCHAR(45) NOT NULL,
  company_name VARCHAR(45) NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  description TEXT NOT NULL,
  PRIMARY KEY (experience_id),
  FOREIGN KEY (resume_id) REFERENCES resume(resume_id),
  CHECK(end_date > start_date)
);

# PROJECT table
CREATE TABLE resumebuilderdb.project (
  project_id INT NOT NULL,
  resume_id VARCHAR(6),
  project_title TEXT NOT NULL,
  project_description TEXT NOT NULL,
  technologies_used TEXT NOT NULL,
  Github_link VARCHAR(45) NULL,
  PRIMARY KEY (project_id),
  FOREIGN KEY (resume_id) REFERENCES resume(resume_id)
);

# JOB APPLICATION Table
CREATE TABLE resumebuilderdb.job_application (
  application_id INT NOT NULL,
  user_id INT NULL,
  Title VARCHAR(45) NOT NULL,
  company VARCHAR(45) NOT NULL,
  application_status VARCHAR(45) NOT NULL,
  application_date DATE NOT NULL,
  PRIMARY KEY (application_id),
  FOREIGN KEY (user_id) REFERENCES user(user_id)
);

# TRIGGER
/*
DELIMITER $$
DROP TRIGGER IF EXISTS userRec $$
CREATE TRIGGER userRec
BEFORE INSERT ON user 
FOR EACH ROW
BEGIN
	INSERT INTO user_record (Action, new_user_id, log_time)
    VALUES("Inserted", NEW.user_id, CURTIME());
END $$
DELIMITER ;
*/

DROP TRIGGER IF EXISTS userRec;

CREATE TRIGGER userRecInsert
BEFORE INSERT ON user 
FOR EACH ROW
INSERT INTO user_record (Action, new_user_id, log_time)
VALUES("Inserted", NEW.user_id, CURTIME());

CREATE TRIGGER userRecDelete
BEFORE DELETE ON user
FOR EACH ROW
INSERT INTO user_record (Action, old_user_id, log_time)
VALUES("Deleted", OLD.user_id, CURTIME());

CREATE TRIGGER userRecUpdate
BEFORE UPDATE ON user
FOR EACH ROW
INSERT INTO user_record (Action, old_user_id, new_user_id, log_time)
VALUES ("Updated", OLD.user_id, NEW.user_id, CURTIME());

SHOW TRIGGERS IN resumebuilderdb;

# PROCEDURE CALLING
# Get table info
CALL get_education_info();
CALL get_resume_info();
CALL get_skill_info();
CALL get_user_info();
CALL get_user_record_info();
CALL get_experience_info();
CALL get_project_info();
CALL get_job_app_info();

# EXECUTION
SELECT * FROM user;

ALTER TABLE skill RENAME TO skills;

ALTER TABLE education RENAME COLUMN grade TO grade_CGPA;
ALTER TABLE user MODIFY COLUMN email VARCHAR(100);
ALTER TABLE resume DROP column resume_data;
ALTER TABLE resume ADD COLUMN achievement_description TEXT;
ALTER TABLE project DROP COLUMN Github_link;

SELECT * FROM resume WHERE resume_id IN (select resume_id FROM skills WHERE skill_name IN ('AWS', 'DSA', 'AIML'));

UPDATE resume SET achievement_description = 
    CASE 
        WHEN resume_id = 'RI1' THEN 'Published a groundbreaking research paper on deep learning optimization techniques.'
	ELSE 'Achievement details not available.'
END;

# FIXES
ALTER TABLE education DROP CHECK education_chk_1;

ALTER TABLE education 
ADD CONSTRAINT education_chk_1
CHECK (grade_CGPA >= 8);

SHOW GRANTS FOR 'DIPANKAR'@'localhost';

GRANT EXECUTE ON PROCEDURE resumebuilderdb.get_job_app_info TO 'DIPANKAR'@'localhost';
FLUSH PRIVILEGES;
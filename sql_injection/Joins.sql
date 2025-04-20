# JOIN Commands
USE resumebuilderdb;

# INNER JOIN: Fetch User details with Resume
SELECT U.user_id, U.name, U.email, R.resume_id, R.languages_known 
FROM User U
INNER JOIN resume R ON U.user_id = R.user_id;

## LEFT JOIN: Fetch all Users and their Job Applications
SELECT U.user_id, U.name, J.title, J.company
FROM User U
LEFT JOIN job_application J ON U.user_id = J.user_id;

# RIGHT JOIN: Fetch all Skills and associated Resumes
SELECT S.skill_id, S.skill_name, R.resume_id
FROM Skills S
RIGHT JOIN resume R ON S.resume_id = R.resume_id;

# FULL OUTER JOIN: Fetch all Users and their Resumes (Union of Left and Right Join)
SELECT U.user_id, U.name, R.resume_id 
FROM User U
LEFT JOIN resume R ON U.user_id = R.user_id
UNION
SELECT U.user_id, U.name, R.resume_id 
FROM User U
RIGHT JOIN resume R ON U.user_id = R.user_id;

# SELF JOIN: Find Users from the same Department
SELECT A.name AS User1, B.name AS User2, A.dept
FROM User A, User B
WHERE A.dept = B.dept AND A.user_id <> B.user_id;

# NATURAL JOIN: Fetch Resume and Education Details
SELECT * FROM resume NATURAL JOIN Education;

# THETA JOIN: Fetch Resumes with more than 1 Experience
SELECT R.resume_id, R.user_id, E.experience_id
FROM resume R, Experience E
WHERE R.resume_id = E.resume_id AND E.experience_id > 1;

# EQUI JOIN: Fetch Projects with Resume ID
SELECT P.project_id, P.project_title, R.resume_id
FROM Project P INNER JOIN resume R ON P.resume_id = R.resume_id;
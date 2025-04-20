-- Create a View of Users with Job Applications
CREATE VIEW UserApplications AS
SELECT U.user_id, U.name, J.title, J.company
FROM User U
INNER JOIN job_application J ON U.user_id = J.user_id;

-- Create or Replace View
CREATE OR REPLACE VIEW ResumeDetails AS
SELECT R.resume_id, R.user_id, S.skill_name, E.degree_name
FROM resume R
LEFT JOIN Skills S ON R.resume_id = S.resume_id
LEFT JOIN Education E ON R.resume_id = E.resume_id;

-- Drop View
DROP VIEW UserApplications;

-- Select from View
SELECT * FROM ResumeDetails;

-- Delete from View
DELETE FROM ResumeDetails WHERE resume_id = 'RI1';

-- Insert into View
INSERT INTO ResumeDetails (resume_id, user_id, skill_name, degree_name)
VALUES ('RI6', 89, 'Cyber Security', 'B.Tech IT');
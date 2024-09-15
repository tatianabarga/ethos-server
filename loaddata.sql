DROP TABLE CircleUser;

CREATE TABLE CircleUser (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    circle_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (circle_id) REFERENCES Circle(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);

CREATE TABLE circle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creator_id INTEGER NOT NULL,
    name VARCHAR(50) NOT NULL,
    FOREIGN KEY (creator_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

ALTER TABLE circle RENAME TO ethosapi_circle;

DELETE FROM ethosapi_user
WHERE id = 10;

DELETE FROM ethosapi_circle
WHERE id = 28;

DELETE FROM ethosapi_circle;

-- Insert into ethosapi_profile without any circle connections
INSERT INTO ethosapi_profile (creator_id, bio, name)
VALUES
(2, 'Experienced Roofing contractor', 'Bobs Roofing'),
(2, 'Expert in construction', 'You Need We Build'),
(3, 'Freelance electrician', 'Zappies Electric'),
(4, 'Plumbing specialist', 'The Pipe Guys'),
(5, 'Roofing expert', 'Gretta Roofs');

-- Insert into ethosapi_user to mimic company employees
INSERT INTO ethosapi_user (name, uid)
VALUES
('Alice Johnson', 'emp001'),
('Bob Smith', 'emp002'),
('Charlie Davis', 'emp003'),
('Dana Lee', 'emp004'),
('Evan Garcia', 'emp005');







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

DELETE FROM ethosapi_circleuser
WHERE id = 2;




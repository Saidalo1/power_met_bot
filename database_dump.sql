CREATE TABLE IF NOT EXISTS generators
(
    id
        INTEGER
        PRIMARY
            KEY
        AUTOINCREMENT,
    name
        TEXT,
    height
        INTEGER,
    length
        INTEGER,
    width
        INTEGER,
    power_kbt
        INTEGER,
    power_kba
        INTEGER,
    fuel_consumption
        INTEGER
);

INSERT INTO generators
VALUES (1, 'AJ-ELLA 250', 1550, 2600, 1100, 210, 250, 19),
       (2, 'AJ – S 330', 1950, 3100, 1100, 260, 330, 28),
       (3, 'AJ – S 275', 1950, 3100, 1100, 250, 250, 250),
       (4, 'AJ – S 385', 2000, 3400, 1600, 308, 385, 71),
       (5, 'AJ – S 440', 2000, 3350, 1400, 352, 440, 65),
       (6, 'AJ – S  525', 2000, 3400, 1600, 430, 525, 70),
       (7, 'AJ – S 640', 2350, 4200, 1900, 520, 640, 96),
       (8, 'AJ – S 825', 2350, 4200, 1900, 720, 750, 77),
       (9, 'AJ – S 950', 2350, 4200, 1900, 720, 950, 80),
       (10, 'AJ – S 1250', 2600, 5200, 2100, 1100, 1250, 118),
       (11, 'AJ – S 700', 2350, 4200, 1900, 520, 640, 62),
       (12, 'AJ – S 825', 2350, 4200, 2350, 720, 750, 77),
       (13, 'AJ – S 1100', 2600, 5200, 2100, 920, 1000, 108),
       (14, 'AJ – S 1375', 2600, 5200, 2100, 1100, 1250, 118),
       (15, 'AJ-ELLA 90', 1350, 1900, 1000, 74, 90, 18),
       (16, 'AJ-ELLA 150', 1600, 2300, 1100, 130, 150, 21),
       (17, 'AJ-ELLA 16', 1250, 1450, 1000, 12, 14, 9),
       (18, 'AJ-ELLA 75', 1350, 1900, 1000, 74, 70, 18),
       (19, 'AJ-ELLA 225', 1550, 2600, 1100, 170, 205, 26),
       (20, 'AJ-ELLA 37', 1300, 1700, 1000, 33, 37, 7),
       (21, 'AJ-ELLA 28', 1250, 1850, 1000, 24, 25, 4),
       (22, 'AJ-ELLA 125', 1600, 2300, 1100, 110, 125, 21);

CREATE TABLE IF NOT EXISTS users_language
(
    id
        INTEGER
        PRIMARY
            KEY,
    chat_id
        BIGINT UNIQUE,
    language
        TEXT
);

END;

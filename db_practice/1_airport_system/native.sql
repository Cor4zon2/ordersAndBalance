CREATE TABLE Passenger (
 	id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);



INSERT INTO PASSENGER (name)
VALUES ('Jack'), ('Bob'), ('Miki')


CREATE TABLE COMPANY (
 	id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);



INSERT INTO COMPANY (name)
VALUES ('AIR DUBAI'), ('CEBU PACIFIC'), ('AIR FRANCE'), ('AIRFLOT');


-- в больших проектах используют множественное число (trips)
CREATE TABLE TRIP (
    ID SERIAL PRIMARY KEY,
    company INT REFERENCES COMPANY(id) NOT NULL,
    plane VARCHAR(255) NOT NULL,
    town_from VARCHAR(255) NOT NULL,
    town_to VARCHAR(255) NOT NULL,
    time_out TIMESTAMP NOT NULL,
    time_in TIMESTAMP NOT NULL,

    CONSTRAINT logical_times CHECK (time_in > time_out)
)

INSERT INTO TRIP (company, plane, town_from, town_to, time_out, time_in)
VALUES (1, 'SUPER UAE', 'DUBAI', 'DOHA',
        '2024-05-15 14:30:00', '2024-05-15 18:30:00')



CREATE TABLE PASS_IN_TRIP (
    ID SERIAL PRIMARY KEY,
    TRIP INT REFERENCES TRIP(ID) NOT NULL,
    PASSENGER INT REFERENCES Passenger(id) NOT NULL,
    PLACE VARCHAR(255) NOT NULL
)
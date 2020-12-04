-- SQLite
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS UserGroup;
CREATE TABLE UserGroup (
  UserType varchar(10) PRIMARY KEY
);

DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
  ID varchar(10) PRIMARY KEY CHECK ((ID LIKE 'G%') OR (ID LIKE 'A%') OR (ID LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')),
  username varchar(50) UNIQUE,
  passCode varchar(40),
  firstName varchar(50),
  lastName varchar(50),
  phoneNo varchar(20) UNIQUE,
  HomeAddress varchar(100),
  postCode varchar(9),
  UserType varchar(10),
  FOREIGN KEY (UserType) REFERENCES UserGroup (UserType) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS available_time;
CREATE TABLE available_time (
  StaffID integer(10) CHECK(StaffID LIKE 'G%'),
  Timeslot datetime,
  PRIMARY KEY (StaffID, Timeslot),
  FOREIGN KEY (StaffID) REFERENCES Users (ID) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS VisitBooking;
CREATE TABLE VisitBooking (
  NHSNo integer(10) CHECK(NHSNo LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
  StaffID integer(10),
  Timeslot datetime,
  Rating int CHECK(Rating >= 0 OR Rating <= 10),
  Confirmed char(1) CHECK(Confirmed IN ('Y', 'N')),
  Attended char(1) CHECK(Attended IN ('Y', 'N')),
  Diagnosis text,
  Notes text,
  PRIMARY KEY (NHSNo, StaffID, Timeslot),
  FOREIGN KEY (StaffID, Timeslot) REFERENCES available_time (StaffID, Timeslot) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (NHSNo) REFERENCES Users (ID) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS perscription;
CREATE TABLE perscription (
  NHSNo integer(10),
  StaffID integer(10),
  Timeslot datetime,
  drugName varchar(70),
  quantity integer,
  drugNotes text,
  PRIMARY KEY (NHSNo, StaffID, Timeslot, drugName),
  FOREIGN KEY (NHSNo, StaffID, Timeslot) REFERENCES VisitBooking (NHSNo, StaffID, Timeslot) ON DELETE CASCADE ON UPDATE CASCADE
);
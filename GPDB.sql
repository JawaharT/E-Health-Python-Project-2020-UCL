-- SQLite
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS UserGroup;
CREATE TABLE UserGroup (
  UserType varchar(10) PRIMARY KEY
);

INSERT INTO UserGroup VALUES ('GP');
INSERT INTO UserGroup VALUES ('Admin');
INSERT INTO UserGroup VALUES ('Patient');

DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
  ID varchar(10) PRIMARY KEY CHECK ((ID LIKE 'G%') OR (ID LIKE 'A%') OR (ID BETWEEN 1000000000 AND 9999999999)),
  username varchar(50) UNIQUE,
  passCode varchar(64),
  firstName BLOB,
  lastName BLOB,
  phoneNo BLOB,
  HomeAddress BLOB,
  postCode BLOB,
  UserType varchar(10),
  Deactivated char(1) CHECK(Deactivated IN ('T','F')),
  FOREIGN KEY (UserType) REFERENCES UserGroup (UserType) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS available_time;
CREATE TABLE available_time (
  StaffID varchar(10) CHECK(StaffID LIKE 'G%'),
  Timeslot datetime,
  PRIMARY KEY (StaffID, Timeslot),
  FOREIGN KEY (StaffID) REFERENCES Users (ID) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Visit;
CREATE TABLE Visit(
  NHSNo varchar(10) CHECK(NHSNo BETWEEN 1000000000 AND 9999999999),
  StaffID varchar(10),
  Timeslot datetime,
  Rating int CHECK(Rating >= 0 OR Rating <= 10),
  Confirmed char(1) CHECK(Confirmed IN ('T', 'F')),
  Attended char(1) CHECK(Attended IN ('T', 'F', 'P')),
  Diagnosis BLOB,
  Notes BLOB,
  PRIMARY KEY (NHSNo, StaffID, Timeslot),
  FOREIGN KEY (StaffID, Timeslot) REFERENCES available_time (StaffID, Timeslot) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (NHSNo) REFERENCES Users (ID) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS perscription;
CREATE TABLE perscription (
  NHSNo varchar(10),
  StaffID varchar(10),
  Timeslot datetime,
  drugName BLOB,
  quantity BLOB,
  Instructions BLOB,
  PRIMARY KEY (NHSNo, StaffID, Timeslot, drugName),
  FOREIGN KEY (NHSNo, StaffID, Timeslot) REFERENCES VisitBooking (NHSNo, StaffID, Timeslot) ON DELETE CASCADE ON UPDATE CASCADE
);

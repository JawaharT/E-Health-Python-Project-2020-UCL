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
  birthday BLOB,
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
  BookingNo INT,
  NHSNo varchar(10) CHECK(NHSNo BETWEEN 1000000000 AND 9999999999),
  StaffID varchar(10),
  Timeslot datetime,
  /*Rating int CHECK(Rating >= 0 OR Rating <= 10),*/
  Confirmed char(1) CHECK(Confirmed IN ('T', 'F', 'P')),
  Attended char(1) CHECK(Attended IN ('T', 'F')),
  Diagnosis BLOB,
  Notes BLOB,
  PRIMARY KEY (BookingNo),
  FOREIGN KEY (StaffID, Timeslot) REFERENCES available_time (StaffID, Timeslot) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (NHSNo) REFERENCES Users (ID) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TABLE IF EXISTS prescription;
CREATE TABLE prescription (
  BookingNo INT,
  drugName BLOB,
  quantity BLOB,
  Instructions BLOB,
  PRIMARY KEY (BookingNo, drugName),
  FOREIGN KEY (BookingNo) REFERENCES VisitBooking (BookingNo) ON DELETE CASCADE ON UPDATE CASCADE
);

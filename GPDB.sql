BEGIN TRANSACTION;
DROP TABLE IF EXISTS "UserGroup";
CREATE TABLE IF NOT EXISTS "UserGroup" (
	"UserType"	varchar(10),
	PRIMARY KEY("UserType")
);
DROP TABLE IF EXISTS "prescription";
CREATE TABLE IF NOT EXISTS "prescription" (
	"PrescriptionNumber"	INTEGER,
	"BookingNo"	INT NOT NULL,
	"drugName"	BLOB NOT NULL,
	"quantity"	BLOB NOT NULL,
	"Instructions"	BLOB NOT NULL,
	PRIMARY KEY("PrescriptionNumber"),
	FOREIGN KEY("BookingNo") REFERENCES "VisitBooking"("BookingNo") ON DELETE CASCADE ON UPDATE CASCADE
);
DROP TABLE IF EXISTS "Users";
CREATE TABLE IF NOT EXISTS "Users" (
	"ID"	varchar(10) CHECK(("ID" LIKE 'G%') OR ("ID" LIKE 'A%') OR ("ID" BETWEEN 1000000000 AND 9999999999)),
	"username"	varchar(50) NOT NULL UNIQUE,
	"passCode"	varchar(64) NOT NULL,
	"birthday"	BLOB,
	"firstName"	BLOB,
	"lastName"	BLOB,
	"phoneNo"	BLOB,
	"HomeAddress"	BLOB,
	"postCode"	BLOB,
	"UserType"	varchar(10) NOT NULL,
	"Deactivated"	char(1) DEFAULT 'T' CHECK("Deactivated" IN ('T', 'F')),
	"LoginCount"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("ID"),
	FOREIGN KEY("UserType") REFERENCES "UserGroup"("UserType") ON DELETE CASCADE ON UPDATE CASCADE
);
DROP TABLE IF EXISTS "Patient";
CREATE TABLE IF NOT EXISTS "Patient" (
	"NHSNo"	varchar(10) CHECK("NHSNo" BETWEEN 1000000000 AND 9999999999),
	"Gender"	char(1) CHECK("Gender" IN ('M', 'F', 'N')),
	"Introduction"	BLOB,
	"Notice"	BLOB,
	PRIMARY KEY("NHSNo"),
	FOREIGN KEY("NHSNo") REFERENCES "Users"("ID") ON DELETE CASCADE ON UPDATE CASCADE
);
DROP TABLE IF EXISTS "available_time";
CREATE TABLE IF NOT EXISTS "available_time" (
	"StaffID"	varchar(10) NOT NULL CHECK("StaffID" LIKE 'G%'),
	"Timeslot"	datetime NOT NULL,
	FOREIGN KEY("StaffID") REFERENCES "Users"("ID") ON DELETE CASCADE ON UPDATE CASCADE
);
DROP TABLE IF EXISTS "GP";
CREATE TABLE IF NOT EXISTS "GP" (
	"ID"	varchar(10),
	"Gender"	char(1) CHECK("Gender" IN ('M', 'F', 'N')),
	"ClinicAddress"	BLOB,
	"ClinicPostcode"	BLOB,
	"Speciality"	BLOB,
	"Introduction"	BLOB,
	"Rating"	INT DEFAULT 0 CHECK("Rating" >= 0 OR "Rating" <= 5),
	PRIMARY KEY("ID"),
	FOREIGN KEY("ID") REFERENCES "Users"("ID") ON DELETE CASCADE ON UPDATE CASCADE
);
DROP TABLE IF EXISTS "Visit";
CREATE TABLE IF NOT EXISTS "Visit" (
	"BookingNo"	INTEGER,
	"NHSNo"	varchar(10) NOT NULL CHECK("NHSNo" BETWEEN 1000000000 AND 9999999999),
	"StaffID"	varchar(10) NOT NULL,
	"Timeslot"	datetime NOT NULL,
	"PatientInfo"	BLOB,
	"Confirmed"	char(1) NOT NULL DEFAULT 'P' CHECK("Confirmed" IN ('T', 'F', 'P')),
	"Attended"	char(1) CHECK("Attended" IN ('T', 'F')),
	"Diagnosis"	BLOB,
	"Notes"	BLOB,
	"Rating"	int DEFAULT 0 CHECK("Rating" >= 0 OR "Rating" <= 5),
	PRIMARY KEY("BookingNo" AUTOINCREMENT),
	FOREIGN KEY("StaffID","Timeslot") REFERENCES "available_time"("StaffID","Timeslot") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("NHSNo") REFERENCES "Patient"("NHSNo") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("StaffID") REFERENCES "GP"("ID") ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO "UserGroup" ("UserType") VALUES ('GP');
INSERT INTO "UserGroup" ("UserType") VALUES ('Admin');
INSERT INTO "UserGroup" ("UserType") VALUES ('Patient');
COMMIT;

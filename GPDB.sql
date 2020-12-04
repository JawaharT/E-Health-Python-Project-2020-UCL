CREATE TABLE "UserGroup" (
  "type" varchar(10) PRIMARY KEY
);

CREATE TABLE "Users" (
  "ID" varchar(10) PRIMARY KEY,
  "username" varchar(50) UNIQUE,
  "password" varchar(40),
  "firstName" varchar(50),
  "lastName" varchar(50),
  "phoneNo" varchar(20),
  "address" varchar(100),
  "postCode" varchar(9),
  "type" varchar(10)
);

CREATE TABLE "availability" (
  "StaffID" integer(10),
  "Timeslot" datetime,
  PRIMARY KEY ("StaffID", "Timeslot")
);

CREATE TABLE "VisitBooking" (
  "NHSNo" integer(10),
  "StaffID" integer(10),
  "Timeslot" datetime,
  "Rating" int,
  "Confirmed" char(1),
  "Attended" char(1),
  "Diagnosis" text,
  "Notes" text,
  PRIMARY KEY ("NHSNo", "StaffID", "Timeslot")
);

CREATE TABLE "perscription" (
  "NHSNo" integer(10),
  "StaffID" integer(10),
  "Timeslot" datetime,
  "drugName" varchar(70),
  "quantity" integer,
  "drugNotes" text,
  PRIMARY KEY ("NHSNo", "StaffID", "Timeslot", "drugName")
);

ALTER TABLE "Users" ADD FOREIGN KEY ("type") REFERENCES "UserGroup" ("type") ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "availability" ADD FOREIGN KEY ("StaffID") REFERENCES "Users" ("ID") ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "VisitBooking" ADD FOREIGN KEY ("StaffID", "Timeslot") REFERENCES "availability" ("StaffID", "Timeslot") ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "VisitBooking" ADD FOREIGN KEY ("NHSNo") REFERENCES "Users" ("ID") ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "perscription" ADD FOREIGN KEY ("NHSNo", "StaffID", "Timeslot") REFERENCES "VisitBooking" ("NHSNo", "StaffID", "Timeslot") ON DELETE CASCADE ON UPDATE CASCADE;


COMMENT ON COLUMN "UserGroup"."type" IS 'admin, GP or patient';

COMMENT ON COLUMN "Users"."ID" IS 'NHSNo or StarffNo starting with G or A';

COMMENT ON COLUMN "Users"."password" IS 'sha';

COMMENT ON COLUMN "availability"."StaffID" IS 'Check if starting with G as it is for GP';

COMMENT ON COLUMN "VisitBooking"."NHSNo" IS 'Check if all number as it is for patient';

COMMENT ON COLUMN "VisitBooking"."StaffID" IS 'Check if starting with G as it is for GP';

COMMENT ON COLUMN "VisitBooking"."Rating" IS 'Constraint: 0 - 10';

COMMENT ON COLUMN "VisitBooking"."Confirmed" IS 'Y or N';

COMMENT ON COLUMN "VisitBooking"."Attended" IS 'Y or N';

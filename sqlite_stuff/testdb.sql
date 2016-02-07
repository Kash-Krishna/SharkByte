BEGIN TRANSACTION;
CREATE TABLE coffees (
  id INTEGER PRIMARY KEY,
  coffee_name TEXT NOT NULL,
  price REAL NOT NULL
);
INSERT INTO "coffees" VALUES(1,'Colombian',7.99);
INSERT INTO "coffees" VALUES(2,'French_Roast',8.99);
INSERT INTO "coffees" VALUES(3,'Espresso',9.99);
INSERT INTO "coffees" VALUES(4,'Colombian_Decaf',8.99);
INSERT INTO "coffees" VALUES(5,'French_Roast_Decaf',9.99);
COMMIT;

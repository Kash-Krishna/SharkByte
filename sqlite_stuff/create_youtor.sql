CREATE TABLE local_youtor (
  magnet_link	TEXT	PRIMARY KEY	NOT NULL,
  torrent_name	TEXT	NOT NULL,
  seeders	INT
);

INSERT INTO "local_youtor" VALUES ('magnet_link_text', 'torrent_name_text', 0);
INSERT INTO "local_youtor" VALUES ('Chung 302', 'The Leviathan', 99);
INSERT INTO "local_youtor" VALUES ('ACM', 'The Shark Tank', 5);

CREATE TABLE local_youtor (
	torrent_name	TEXT	NOT NULL,
	file_size	REAL,
	seeders		INT,
	leechers	INT,
	uploader	TEXT,
	upload_date_time TEXT,	
	magnet_link	TEXT	PRIMARY KEY	NOT NULL
);

/*
magnet_link	TEXT	PRIMARY KEY	NOT NULL,
  torrent_name	TEXT	NOT NULL,
  seeders		INT
);

INSERT INTO "local_youtor" VALUES ('magnet_link_text', 'torrent_name_text', 0);
INSERT INTO "local_youtor" VALUES ('Chung 302', 'The Leviathan', 99);
INSERT INTO "local_youtor" VALUES ('ACM', 'The Shark Tank', 5);
*/

INSERT INTO "local_youtor" VALUES ('kevin', '999', '888', '777', 'kevin_bot', ' ', 'kevin_link');
INSERT INTO "local_youtor" VALUES ('rachel', '888', '777', '999', 'rachel_bot', ' ', 'rachel_link');
INSERT INTO "local_youtor" VALUES ('kash', '777', '999', '888', 'kash_bot', ' ', 'kash_link');
INSERT INTO "local_youtor" VALUES ('nub', '1', '2', '3', 'bot', ' ', 'nub_link');

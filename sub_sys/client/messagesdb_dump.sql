CREATE TABLE messages 
            (msg_id INT PRIMARY KEY,
             time_sent TEXT NOT NULL,
             msg TEXT, 
             sender_uid TEXT NOT NULL, 
             tag TEXT);
CREATE TABLE messages2 (msg_id TEXT PRIMARY KEY NOT NULL, msg TEXT, uid_to TEXT, uid_from TEXT, time TEXT);
INSERT INTO "messages2" VALUES('100','hello','1111','0','2016-03-09 16:17:12');
INSERT INTO "messages2" VALUES('101',':)','1111','0','2016-03-09 16:17:15');
INSERT INTO "messages2" VALUES('102','found a torrent you might want','1111','0','2016-03-09 16:18:32');
INSERT INTO "messages2" VALUES('103','sup?','1111','2222','2016-03-09 16:23:48');

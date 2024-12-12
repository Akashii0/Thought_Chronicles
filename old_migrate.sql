BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "blogs" (
	"id"	INTEGER NOT NULL,
	"title"	VARCHAR NOT NULL,
	"body"	VARCHAR NOT NULL,
	"created_at"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"owner_id"	INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("owner_id") REFERENCES "users"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"author"	VARCHAR NOT NULL,
	"password"	VARCHAR NOT NULL,
	"created_at"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	UNIQUE("author"),
	PRIMARY KEY("id")
);
INSERT INTO "blogs" VALUES (1,'Hi','First time huh?','2024-12-03 18:21:25',1);
INSERT INTO "blogs" VALUES (2,'Let''s FUCKKING GOOO!!','heheheeheh we finally did it!!!!!!!!!!!!!!!','2024-12-03 18:27:16',1);
INSERT INTO "blogs" VALUES (3,'Yoooo','Good work 🔥😮‍💨','2024-12-03 18:48:58',1);
INSERT INTO "blogs" VALUES (4,'Yokoso ','Watashi wa soul society 

Hado no 90: kurohistugi','2024-12-03 18:52:20',5);
INSERT INTO "blogs" VALUES (5,'Heyuy','Ndndnd','2024-12-03 18:53:37',6);
INSERT INTO "blogs" VALUES (6,'Sup','Cool shit','2024-12-03 18:54:05',6);
INSERT INTO "blogs" VALUES (7,'Sinm','I think brown is sooooo cool y''know ','2024-12-03 19:00:34',7);
INSERT INTO "blogs" VALUES (8,'The Untold Chapters','Because you are a book upon which I have stumbled,
with chapters no one has ever dared to explore—
chapters that make the heart shed blood,
for they hold nothing but the tale of a maiden
trying her best to bridge the gap between her past and future.
Heavy are the tears shed upon these chapters,
for they have left a stain on this book we call life.
Many have tried to read this book, yet many have given up along the way.
But will I be able to watch as you write your name in the sands of time?
That I do not know.
But I must say,
I wish to be by your side.

','2024-12-03 19:14:26',8);
INSERT INTO "blogs" VALUES (9,'I wan cum','Almost there','2024-12-03 23:29:51',10);
INSERT INTO "blogs" VALUES (10,'My prick dey itch me','Akeem come help me scratch my prick','2024-12-03 23:30:23',10);
INSERT INTO "blogs" VALUES (11,'Kindred Scars','
Souls have been found to swim in the river of time.

Fated are two souls whose differences, though vast as the galaxies,
possess a past to which they can say is a scar on their hearts.
Though different, they possess a past to which they can talk about—
a past to which they tend to be judged,
a past that has shaped them into who they are.

Traumatic as it may sound,
they find solace in the arms of each other.
For indeed, those who have been hurt are the kindest souls.

Scars possessing mysteries are unraveled as they spend time together.

Will they be able to come together as one?
Or will their differences get the best of them?','2024-12-05 18:00:47',8);
INSERT INTO "blogs" VALUES (12,'This is a test','I am him!
The one true developer! ','2024-12-11 06:37:59',24);
INSERT INTO "users" VALUES (1,'Akashi','$2b$12$4KeQkXPQKeOHYPIYiqoZKefpurppgikBqAQJ34KZLDWJ5ycHKjNUu','2024-12-03 18:21:05');
INSERT INTO "users" VALUES (2,'Tenix','$2b$12$FEEie9miTLfXj05PEHHxbu9Gq6Q2uTVGvc30HvI8VJG4sYp2DIVO2','2024-12-03 18:37:50');
INSERT INTO "users" VALUES (3,'Batman','$2b$12$4VBeRH9BbUBqUkNpaGMZxuXps3oUOOdYfFFrI6.ytKOOM3Sx1YHPy','2024-12-03 18:45:41');
INSERT INTO "users" VALUES (4,'Victor','$2b$12$61jskIqLO8swA6l2XOExxub4ziNfZKhnEfMDa8da3XraHN8UD1q3G','2024-12-03 18:45:53');
INSERT INTO "users" VALUES (5,'Akaza','$2b$12$7XXzN1X7NAlT2ELwoVmKF.6xO5LYX9TTGfox6cXFHSW.Pl5GKtANW','2024-12-03 18:47:38');
INSERT INTO "users" VALUES (6,'Zhadow','$2b$12$GvEvr3hRP2OiQLPnEV5CJeKYGfidsPe5BBMbs/8rPQxZ6bvhsWtGm','2024-12-03 18:50:15');
INSERT INTO "users" VALUES (7,'Sinm','$2b$12$Bhbk9lgAE1c3cCJb2VvQ8OKdmmTzVhZOsN.AkE4R7c1n99hY/w3a.','2024-12-03 18:55:37');
INSERT INTO "users" VALUES (8,'nuels_rhythm','$2b$12$Hhq/V/qHvBKNKLuZpt26vuQPEwyiMEsCG9VFfuQ6I6KKlUIyXEltq','2024-12-03 19:11:04');
INSERT INTO "users" VALUES (9,'ok','$2b$12$/Dqs4.ta0KIL8AcBGpOliu7K8tV8pMNKQi9jv3iOspH7KgYDrdQBi','2024-12-03 20:45:47');
INSERT INTO "users" VALUES (10,'myprick@gmail.com','$2b$12$mGZ1ZOt/S.y.cfD2w9d05eKTmDQNb2nXFPLyDCTvoqAK/P785EjMu','2024-12-03 23:28:27');
INSERT INTO "users" VALUES (11,'o.joeade@gmail.com','$2b$12$6GIHVJm2p0GlvWsXfUXRMeeszwtwrUwCJ1da9ZZlHdB.PHuFxC6wi','2024-12-03 23:42:30');
INSERT INTO "users" VALUES (12,'Olamide2000','$2b$12$OxWjXYJdEJBuXhL6A6N5m.3Jwh6Ub5.TUmP3mYKDEFHTT74.f0zRq','2024-12-03 23:43:18');
INSERT INTO "users" VALUES (13,'Olamide2008','$2b$12$NlS.hNSvXd3lv.yxLTOR6eXsz6w15VWxE3bdDUzVQ8lq3PUIZAcr6','2024-12-03 23:44:10');
INSERT INTO "users" VALUES (14,'Vuhkjjɓbg','$2b$12$A6KiLgwKmB1qIIauBT5sKOBM8nT8ah2IpIwAOA1dp1fD44iSC4Qo6','2024-12-04 04:05:50');
INSERT INTO "users" VALUES (15,'uahj@gmail.com','$2b$12$HmBmaJIN2UjPPDl1cSAH.emzsmdjIYRBUlnsiTAjNkbjpxJkpWYpK','2024-12-04 10:40:09');
INSERT INTO "users" VALUES (16,'Astro','$2b$12$YsJwhvuMSaVopOZve.U90OCLazqlz1WUm4UZfZzM5XA4bBf2h0HQu','2024-12-08 14:47:20');
INSERT INTO "users" VALUES (17,'Julia','$2b$12$7EFowEr.pxPVSMdEOxecAuH3GMh6UHtJwWqyDtTvrM8q0F/ivqLaO','2024-12-08 16:24:03');
INSERT INTO "users" VALUES (18,'water','$2b$12$dVdtJy5Fkb/MWuQ2YHaWKeVxRftcfxruaJ30hSJnBO7YEpJvHnOem','2024-12-08 22:32:18');
INSERT INTO "users" VALUES (19,'were','$2b$12$h4nSq0yQBT34SOHMxJkeoebZrTJRT7N9h/2Pfi9tKsuf.NSN5s5Be','2024-12-08 22:32:49');
INSERT INTO "users" VALUES (20,'Hhehdhdhd@gmail.com','$2b$12$XQAKKd54cVxx.vWc6psUw.UMKUfwBlOXKT4MK/kNXuGDxKaJHOEZa','2024-12-08 22:44:31');
INSERT INTO "users" VALUES (21,'kai22','$2b$12$ocagHUxOEQrza/UCskHF1OKw4LSZfaefSVZWh1.3WCunD3CV0F3hi','2024-12-09 10:58:33');
INSERT INTO "users" VALUES (22,'Ali','$2b$12$PvNBiyKlR5n.SmcHAvALdemnVj1r.HS3XWCHsBYrxgVxzkXuAcA.y','2024-12-09 13:04:23');
INSERT INTO "users" VALUES (23,'ItzFritz','$2b$12$kt4ozLvnutTb1xoE6dlyyejIX99VabP9mTL1wbXPuGC.SJhDzH1Au','2024-12-09 14:53:08');
INSERT INTO "users" VALUES (24,'philipthedeveloper','$2b$12$hVYj2ieNh07l9NI/JgGWiOH4.vJ5pq9xl3G8TJcPI.oBAonLMkazq','2024-12-11 06:27:34');
COMMIT;

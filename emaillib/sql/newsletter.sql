-- t_email definition

CREATE TABLE "t_email" (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	addr VARCHAR(80) NOT NULL,
	latestSentAt DATE,
	sentCount INTEGER DEFAULT (0),
	unsubscribed BOOLEAN DEFAULT (0)
);

CREATE UNIQUE INDEX t_email_addr_IDX ON t_email (addr);


-- t_history definition

CREATE TABLE "t_history" (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	"from" VARCHAR(80) NOT NULL,
	"to" VARCHAR(80) NOT NULL,
	sentAt DATE,
	subject VARCHAR(100)
);
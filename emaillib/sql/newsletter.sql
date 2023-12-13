-- t_email definition

CREATE TABLE "t_email" (
	"address" VARCHAR(80),
	latestSentAt DATE,
	sentCount INTEGER DEFAULT (0),
	unsubscribed BOOLEAN DEFAULT (0)
);

CREATE INDEX email_address_IDX ON "t_email" (address);
CREATE UNIQUE INDEX t_email_address_IDX ON t_email (address);

-- t_history definition

CREATE TABLE "t_history" (
	id INT,
	"from" VARCHAR(80),
	"to" VARCHAR(80),
	sentAt DATE,
	subject VARCHAR(100)
);

CREATE UNIQUE INDEX history_id_IDX ON "t_history" (id);
CREATE UNIQUE INDEX t_history_id_IDX ON t_history (id);
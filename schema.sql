CREATE TABLE app_user (
	id INTEGER NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password VARCHAR(1024) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email), 
	UNIQUE (password)
);


CREATE TABLE project (
	id INTEGER NOT NULL, 
	owner INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner) REFERENCES app_user (id)
);


CREATE TABLE file (
	id INTEGER NOT NULL, 
	owner INTEGER, 
	containing_project INTEGER, 
	data BYTEA, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner) REFERENCES app_user (id), 
	FOREIGN KEY(containing_project) REFERENCES project (id)
);

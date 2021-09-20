CREATE TABLE "FileProject" (
	file_id INTEGER NOT NULL, 
	project_id INTEGER NOT NULL, 
	PRIMARY KEY (file_id, project_id), 
	FOREIGN KEY(file_id) REFERENCES "Files" (id), 
	FOREIGN KEY(project_id) REFERENCES "Projects" (id)
);


CREATE TABLE "AppUsers" (
	id INTEGER NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password VARCHAR(1024) NOT NULL, 
	is_admin BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (password)
);


CREATE TABLE "Projects" (
	id INTEGER NOT NULL, 
	owner INTEGER, 
	name VARCHAR(80), 
	published BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner) REFERENCES "AppUsers" (id), 
	UNIQUE (name)
);


CREATE TABLE "Files" (
	id INTEGER NOT NULL, 
	owner INTEGER, 
	data BLOB, 
	name VARCHAR(80), 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner) REFERENCES "AppUsers" (id)
);


CREATE TABLE "Comments" (
	id INTEGER NOT NULL, 
	sender INTEGER, 
	containing_project INTEGER, 
	content VARCHAR(1024) NOT NULL, 
	sent DATETIME DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sender) REFERENCES "AppUsers" (id), 
	FOREIGN KEY(containing_project) REFERENCES "Projects" (id)
);


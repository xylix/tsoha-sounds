CREATE TABLE fileproject (
	file_id INTEGER NOT NULL, 
	project_id INTEGER NOT NULL, 
	PRIMARY KEY (file_id, project_id), 
	FOREIGN KEY(file_id) REFERENCES files (id), 
	FOREIGN KEY(project_id) REFERENCES projects (id)
);


CREATE TABLE appusers (
	id SERIAL NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password VARCHAR(1024) NOT NULL, 
	is_admin BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (password)
);


CREATE TABLE projects (
	id SERIAL NOT NULL, 
	owner INTEGER, 
	name VARCHAR(80), 
	published BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner) REFERENCES appusers (id), 
	UNIQUE (name)
);


CREATE TABLE files (
	id SERIAL NOT NULL, 
	owner INTEGER, 
	data BYTEA, 
	name VARCHAR(80), 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner) REFERENCES appusers (id)
);


CREATE TABLE comments (
	id SERIAL NOT NULL, 
	sender INTEGER, 
	containing_project INTEGER, 
	content VARCHAR(1024) NOT NULL, 
	sent TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sender) REFERENCES appusers (id), 
	FOREIGN KEY(containing_project) REFERENCES projects (id)
);

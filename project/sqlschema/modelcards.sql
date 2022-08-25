

CREATE TABLE dataset (
	name TEXT, 
	link TEXT, 
	sensitive BOOLEAN, 
	graphics TEXT, 
	PRIMARY KEY (name, link, sensitive, graphics)
);

CREATE TABLE graphic (
	name TEXT, 
	image TEXT, 
	PRIMARY KEY (name, image)
);

CREATE TABLE graphics (
	description TEXT, 
	collection TEXT, 
	PRIMARY KEY (description, collection)
);

CREATE TABLE "ModelCard" (
	schema_version TEXT, 
	model_details TEXT NOT NULL, 
	model_parameters TEXT, 
	quantitative_analysis TEXT, 
	considerations TEXT, 
	PRIMARY KEY (schema_version, model_details, model_parameters, quantitative_analysis, considerations)
);

CREATE TABLE owner (
	name TEXT, 
	contact TEXT, 
	PRIMARY KEY (name, contact)
);

CREATE TABLE performance_metric (
	type TEXT NOT NULL, 
	value TEXT, 
	confidence_interval TEXT, 
	threshold FLOAT, 
	slice TEXT, 
	PRIMARY KEY (type, value, confidence_interval, threshold, slice)
);

CREATE TABLE risk (
	name TEXT, 
	mitigation_strategy TEXT, 
	PRIMARY KEY (name, mitigation_strategy)
);

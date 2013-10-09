DROP TABLE IF EXISTS retail.premiums;
DROP SEQUENCE IF EXISTS retail.premium_ids_sequence;
DROP TABLE IF EXISTS retail.run_parameters;
DROP SEQUENCE IF EXISTS retail.parameter_ids_sequence;
DROP TABLE IF EXISTS retail.customer_demand;
DROP TABLE IF EXISTS retail.customers;
DROP SEQUENCE IF EXISTS retail.customer_ids_sequence;
DROP TABLE IF EXISTS retail.markets;

CREATE TABLE retail.markets
(
  market CHAR(15) NOT NULL PRIMARY KEY,
  country_code CHAR(2) NOT NULL,
  commodity CHAR(10) NOT NULL
);

INSERT INTO retail.markets VALUES('nbp', 'UK', 'gas');

CREATE SEQUENCE retail.customer_ids_sequence;
CREATE TABLE retail.customers
(
  customer_id integer NOT NULL PRIMARY KEY DEFAULT NEXTVAL('retail.customer_ids_sequence'),
  name CHAR(30) NOT NULL,
  market CHAR(15) NOT NULL REFERENCES retail.markets(market),
  image64 bytea
);

CREATE TABLE retail.customer_demand
(
  customer_id INTEGER NOT NULL REFERENCES retail.customers(customer_id),
  datetime TIMESTAMP NOT NULL,
  value FLOAT(19) NOT NULL,
  CONSTRAINT customer_demand_pkey PRIMARY KEY (customer_id, datetime)
);

CREATE SEQUENCE retail.parameter_ids_sequence;
CREATE TABLE retail.run_parameters
(
  run_id integer NOT NULL PRIMARY KEY DEFAULT NEXTVAL('retail.parameter_ids_sequence'),
  parameters bytea NOT NULL,
  db_upload_datetime TIMESTAMP NOT NULL
);

CREATE SEQUENCE retail.premium_ids_sequence;
CREATE TABLE retail.premiums
(
  premium_id integer NOT NULL PRIMARY KEY DEFAULT NEXTVAL('retail.premium_ids_sequence'),
  run_id integer NOT NULL REFERENCES retail.run_parameters(run_id),
  customer_id integer NOT NULL REFERENCES retail.customers(customer_id),
  contract_start_date_utc TIMESTAMP NOT NULL,
  contract_end_date_utc TIMESTAMP NOT NULL,
  premium FLOAT(19) NOT NULL
);
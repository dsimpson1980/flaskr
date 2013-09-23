drop table if exists entries;
drop table if exists retail.demand;
drop table if exists retail.customers;
drop sequence if exists retail.customer_ids_sequence;
drop table if exists retail.markets;

create sequence entries_sequence;
create table entries (
  id integer primary key default nextval(entries_sequence) not null,
  title text not null,
  text text not null
);

create table retail.markets (
  market char(15) primary key,
  country_code char(2) not null,
  commodity char(10) not null
);

create sequence retail.customer_ids_sequence;
create table retail.customers (
  customer_id integer primary key default not null,
  name varchar not null,
  market char(15) not null references retail.markets(market)
);

create table retail.demand (
  customer_id integer not null references retail.customers(customer_id),
  datetime_utc timestamp not null,
  value float not null,
  primary key(customer_id, datetime_utc)
);


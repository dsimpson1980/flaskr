drop table if exists entries;
drop table if exists customers;
drop table if exists markets;
drop table if exists demand;

create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

create table markets (
  market string primary key,
  country_code string not null,
  commodity string not null
);

create table customers (
  customer_id integer primary key autoincrement,
  name string not null,
  market string not null,
  foreign key(market) references markets(market)
);

create table demand (
  customer_id integer not null ,
  datetime_utc datetime not null,
  value not null,
  primary key(customer_id, datetime_utc),
  foreign key(customer_id) references customers(customer_id)
);


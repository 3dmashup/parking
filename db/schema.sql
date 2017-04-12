
drop schema if exists ridecell cascade;
create schema ridecell;

set search_path to ridecell, public;


drop table if exists parking_spot cascade;
create table parking_spot
(
  id  serial not null primary key,
  nearest_address text not null,
  lat real not null,
  long real not null,
  updated_at timestamp not null default now(),
  created_at timestamp not null default now()
);

create index parking_spot_location_idx on   parking_spot  (lat, long) ;

drop table if exists parking_sport_reservation;

create table parking_spot_reservation
(
   id   serial not null primary key,
   spot_id integer not null references parking_spot(id),
   user_id  integer not null,
   duration tsrange not null,
   updated_at timestamp not null default now(),
   created_at timestamp not null default now()
);

create index tsrange_idx on parking_spot_reservation using gist  (duration);


-- load data

set search_path to ridecell, public;

delete from parking_spot  where  1 = 1;
insert into parking_spot ( nearest_address, lat, long)  values

( '123 bryant', 38.0, 122.4),
( '123 bryant', 38.1, 122.4),
( '123 bryant', 38.2, 122.4),
( '123 bryant', 38.3, 122.4),
( '123 bryant', 38.4, 122.4);

select * from parking_spot;

delete from parking_spot_reservation  where 1=1;

insert into parking_spot_reservation (spot_id, user_id, duration ) values

(  1, 1, '[2017-04-10 12:00:00,  2017-04-10 15:00:00]'),
(  4,1, '[2017-04-10 15:00:00,  2017-04-10 19:00:00]');

select * from parking_spot_reservation;





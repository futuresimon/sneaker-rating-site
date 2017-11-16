drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null
);

drop table if exists reviews;
create table reviews (
  id integer primary key autoincrement,
  review text,
  rating integer not null,
  user_id integer,
  sneaker_id integer,
  display integer not null,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (sneaker_id) REFERENCES sneakers(id)
);

drop table if exists sneakers;
create table sneakers (
  id integer primary key autoincrement,
  name text,
  image_path text,
  user_id integer,
  display integer not null,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

drop table if exists favorites;
create table favorites (
  id integer primary key autoincrement,
  user_id integer,
  sneaker_id integer,
  display integer not null,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (sneaker_id) REFERENCES sneakers(id)
)

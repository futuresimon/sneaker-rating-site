drop table if exists users;
create table users (
  id integer primary key autoincrement,
  is_admin integer not null,
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

drop table if exists admin_reviews;
create table admin_reviews (
  id integer primary key autoincrement,
  website text,
  review text,
  user_id integer,
  sneaker_id integer,
  display integer not null,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (sneaker_id) REFERENCES sneakers(id)
);

drop table if exists messages;
create table messages (
  id integer primary key autoincrement,
  message_body text,
  sender_id integer,
  reciever_id integer,
  FOREIGN KEY (sender_id) REFERENCES users(id),
  FOREIGN KEY (reciever_id) REFERENCES users(id)
);

drop table if exists sneakers;
create table sneakers (
  id integer primary key autoincrement,
  name text,
  brand text,
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

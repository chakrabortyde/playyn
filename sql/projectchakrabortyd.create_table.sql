create database if not exists playyn;

use playyn;

create table if not exists track (
	track_id int primary key auto_increment,
    track_no int,
    track_title varchar(300),
    track_release_date datetime,
    language_id int,
    track_price int,
    duration_ms int,
    explicit boolean,
    track_icon varchar(1000)
);

create table if not exists audio_features (
	track_id int unique,
	acousticness float,
    danceability float,
    energy float,
    instrumentalness float,
    keynote float,
    liveness float,
    loudness float,
    scale float,
    speechiness float,
    tempo float,
    valence float,
    foreign key (track_id) references track(track_id) on update no action on delete no action
);

create table if not exists album (
	album_id int primary key auto_increment,
    album_name varchar(300),
    album_release_date datetime,
    album_icon varchar(1000)
);

create table if not exists album_track (
	album_id int,
    track_id int,
    primary key (album_id, track_id),
    foreign key (album_id) references album(album_id) on update cascade on delete cascade,
    foreign key (track_id) references track(track_id) on update cascade on delete cascade
);

create table if not exists genre (
	genre_id int primary key,
    genre_title varchar(300)
);

create table if not exists track_genre (
	track_id int,
    genre_id int,
    primary key (track_id, genre_id),
    foreign key (track_id) references track(track_id) on update cascade on delete cascade,
    foreign key (genre_id) references genre(genre_id) on update cascade on delete cascade
);

create table if not exists available_market (
	market_id int primary key auto_increment,
    market_code varchar(2) unique,
    market_name varchar(300)
);

create table if not exists track_market (
	track_id int,
    market_id int,
    primary key (track_id, market_id),
    foreign key (track_id) references track(track_id) on update cascade on delete cascade,
    foreign key (market_id) references available_market(market_id) on update cascade on delete cascade
);

create table if not exists album_market (
	album_id int,
    market_id int,
    primary key (album_id, market_id),
    foreign key (album_id) references album(album_id) on update cascade on delete cascade,
    foreign key (market_id) references available_market(market_id) on update cascade on delete cascade
);

create table if not exists address (
	address_id int primary key,
    address_line_1 varchar(300),
    address_line_2 varchar(300),
    city varchar(300),
    state varchar(300),
    country varchar(300),
    zipcode int
);

create table if not exists country_code (
	country_name varchar(300) primary key,
    numeric_code int
);

create table if not exists languages (
	language_id int primary key,
    language_name varchar(300)
);

create table if not exists artist (
	artist_id int primary key auto_increment,
	first_name varchar(300),
    last_name varchar(300),
	gender varchar(300),
    date_of_birth date,
    address_id int,
    phone_no varchar(300) unique,
    password varchar(300),
    email_address varchar(300) unique,
    foreign key (address_id) references address(address_id) on update cascade on delete cascade
);

create table if not exists proficiency (
	proficiency_id int primary key,
    proficiency_name varchar(300)
);

create table if not exists artist_proficiency (
	artist_id int,
    proficiency_id int,
    primary key (artist_id, proficiency_id),
    foreign key (artist_id) references artist(artist_id) on update cascade on delete cascade,
    foreign key (proficiency_id) references proficiency(proficiency_id) on update cascade on delete cascade
);

create table if not exists band (
	band_id int primary key auto_increment,
    band_name varchar(300)
);

create table if not exists band_artist (
	band_id int,
    artist_id int,
    primary key (band_id, artist_id),
    foreign key (band_id) references band(band_id) on update cascade on delete cascade,
    foreign key (artist_id) references artist(artist_id) on update cascade on delete cascade
);

create table if not exists track_band (
	track_id int,
    band_id int,
    primary key (track_id, band_id),
    foreign key (track_id) references track(track_id) on update cascade on delete cascade,
    foreign key (band_id) references band(band_id) on update cascade on delete cascade
);

create table if not exists album_band (
	album_id int,
    band_id int,
    primary key (album_id, band_id),
    foreign key (album_id) references album(album_id) on update cascade on delete cascade,
    foreign key (band_id) references band(band_id) on update cascade on delete cascade
);

create table if not exists customer (
	customer_id int primary key auto_increment,
	first_name varchar(300),
    last_name varchar(300),
	gender varchar(300),
    date_of_birth date,
    address_id int,
    phone_no varchar(300) unique,
    password varchar(300),
    email_address varchar(300) unique,
    foreign key (address_id) references address(address_id) on update cascade on delete cascade
);
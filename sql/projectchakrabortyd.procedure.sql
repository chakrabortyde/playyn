use playyn;

drop procedure if exists fetch_user_profile;
delimiter //
create procedure fetch_user_profile(in r varchar(30),
									in e_mail varchar(300))
begin
	if (r = 'customer') then
		select * from customer natural join address where email_address = e_mail;
	elseif (r = 'artist') then
		select * from artist natural join address where email_address = e_mail;
	end if;
end //
delimiter ;

drop procedure if exists update_user_profile;
delimiter //
create procedure update_user_profile(in r varchar(30),
									 in e_mail varchar(300),
                                     in f_name varchar(300),
                                     in l_name varchar(300),
                                     in g varchar(300),
                                     in dob date,
                                     in a_id int,
                                     in p_id int)
begin
	declare user_id int;
	if (r = 'customer') then
		if (f_name != '') then
			update customer set first_name = f_name where email_address = e_mail;
		end if;
        if (l_name != '') then
			update customer set last_name = l_name where email_address = e_mail;
		end if;
        if (g != '') then
			update customer set gender = g where email_address = e_mail;
		end if;
        update customer set date_of_birth = dob where email_address = e_mail;
        if (a_id != 0) then
			update customer set address_id = a_id where email_address = e_mail;
		end if;
	elseif (r = 'artist') then
		if (f_name != '') then
			update artist set first_name = f_name where email_address = e_mail;
		end if;
        if (l_name != '') then
			update artist set last_name = l_name where email_address = e_mail;
		end if;
        if (g != '') then
			update artist set gender = g where email_address = e_mail;
		end if;
        update artist set date_of_birth = dob where email_address = e_mail;
        if (a_id != 0) then
			update artist set address_id = a_id where email_address = e_mail;
		end if;
        if (p_id != '') then
			select artist_id into user_id from artist where email_address=e_mail;
			insert ignore into artist_proficiency values (user_id, p_id);
		end if;
	end if;
end //
delimiter ;

drop procedure if exists get_all_addresses;
delimiter //
create procedure get_all_addresses()
begin
	select * from address;
end //
delimiter ;

drop procedure if exists get_all_tracks;
delimiter //
create procedure get_all_tracks()
begin
	select track_icon, track_no, track_title,
		time_since_release(track_release_date) as track_release,
		concat("$", track_price) as track_price, millis_to_duration(duration_ms) as duration,
		language_name, album_name, band_name
    from track
    natural join languages
    natural join album_track
    natural join album
    natural join album_band
    natural join band;
end //
delimiter ;

drop procedure if exists get_featured_tracks;
delimiter //
create procedure get_featured_tracks()
begin
	select track_icon, track_title,
		time_since_release(track_release_date) as track_release, 
		millis_to_duration(duration_ms) as duration, album_name, band_name
    from track
    natural join album_track
    natural join album
    natural join album_band
    natural join band
    limit 6;
end //
delimiter ;

drop procedure if exists get_all_albums;
delimiter //
create procedure get_all_albums()
begin
	select album_name,
		time_since_release(album_release_date) as album_release,
		album_icon, band_name, count(track_id) as track_count
    from album
    natural join album_band 
    natural join band 
    natural join album_track;
end //
delimiter ;

drop procedure if exists get_featured_albums;
delimiter //
create procedure get_featured_albums()
begin
	select album_name, band_name,
		time_since_release(album_release_date) as album_release,
		count(*) as num_tracks, album_icon
    from album
    natural join album_band
    natural join band
    natural join album_track
    limit 6;
end //
delimiter ;

drop procedure if exists get_all_artists;
delimiter //
create procedure get_all_artists()
begin
	select concat(first_name, " ", last_name) as name, gender, 
		trim(leading '0' from (date_format(from_days(datediff(curdate(), date_of_birth)), "%Y"))) as age,
		concat(city, ", ", state, ", ", country) as current_city, phone_no, email_address,
		ifnull(band_name, "") as band_name
    from artist
    natural join address
    left join band_artist
    using (artist_id)
    left join band
    using (band_id);
end //
delimiter ;

drop procedure if exists get_featured_bands;
delimiter //
create procedure get_featured_bands()
begin
	select band_name, group_concat(concat(first_name, " ", last_name)) as band_members
    from band
    natural join band_artist
    natural join artist
    group by band_id
    limit 6;
end //
delimiter ;

drop procedure if exists get_all_country_codes;
delimiter //
create procedure get_all_country_codes()
begin
	select country_name, numeric_code
    from country_code
    order by country_name;
end //
delimiter ;

drop procedure if exists get_all_available_artists;
delimiter //
create procedure get_all_available_artists(in a_id int)
begin
	select *
    from artist
    where artist_id
    not in
    (select artist_id from band_artist)
    and
    artist_id != a_id;
end //
delimiter ;

drop procedure if exists get_band_details;
delimiter //
create procedure get_band_details(in a_id int)
begin
	select band_id, band_name, 
		concat(first_name, " ", last_name) as member,
		group_concat(ifnull(proficiency_name, "")) as proficiency
    from (select band_id, band_name
			from band_artist
			natural join band
			where artist_id = a_id) as b
    natural join band_artist
    natural join artist
    left join artist_proficiency
    using (artist_id)
    left join proficiency
    using (proficiency_id)
    group by artist_id;
end //
delimiter ;